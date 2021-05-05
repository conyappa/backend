import threading as th

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from accounts.models import Device
from main.permissions import (
    InternalCommunication,
    ListOwnership,
    ObjectOwnership,
    ReadOnly,
)
from main.versioning import VersioningMixin

from .models import Draw, LuckyTicket
from .pagination import TicketPagination
from .serializers import (
    DrawSerializer,
    LuckyTicketSerializer,
    PrizeField,
    PrizeFieldVersion1,
    TicketSerializer,
    TicketSerializerVersion1,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def draws_metadata(request, **kwargs):
    if request.version == "v1":
        prize_field = PrizeFieldVersion1()
    else:
        prize_field = PrizeField()

    return Response(
        data={
            "prizes": {
                str(number_of_matches): prize_field.to_representation(number_of_matches)
                for number_of_matches in range(8)
            },
        },
        status=HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([InternalCommunication])
def choose_result(request, **kwargs):
    draw = Draw.objects.ongoing()
    draw.choose_result()

    serializer_context = {"request": request}
    serializer = DrawSerializer(instance=draw, context=serializer_context)

    response = Response(data=serializer.data, status=HTTP_200_OK)

    thread = th.Thread(
        target=Device.objects.all().send_push_notification,
        kwargs={"body": "Ya está disponible el número de hoy."},
    )
    thread.start()

    return response


class GenericDrawView(GenericAPIView):
    queryset = Draw.objects
    serializer_class = DrawSerializer


class DrawListView(CreateModelMixin, GenericDrawView):
    permission_classes = [InternalCommunication]

    def post(self, request, **kwargs):
        response = self.create(request)

        thread = th.Thread(
            target=Device.objects.all().send_push_notification,
            kwargs={"body": "Se han generado los boletos del sorteo."},
        )
        thread.start()

        return response


class OngoingDrawView(RetrieveModelMixin, GenericDrawView):
    permission_classes = [IsAuthenticated & ReadOnly]

    def get_object(self):
        return Draw.objects.ongoing()

    def get(self, request, **kwargs):
        return self.retrieve(request)


class GenericTicketView(VersioningMixin, GenericAPIView):
    pagination_class = TicketPagination

    def get_serializer_class(self):
        if self.request.version == "v1":
            return TicketSerializerVersion1
        return TicketSerializer


class UserTicketsView(ListModelMixin, GenericTicketView):
    permission_classes = [IsAuthenticated & ListOwnership & ReadOnly]

    def initial(self, request, user_id, **kwargs):
        User = get_user_model()
        self.user = get_object_or_404(User.objects, pk=user_id)
        self.owners = {self.user}

        return super().initial(request, user_id, **kwargs)

    def get_queryset(self):
        return self.user.current_tickets.order_by("-number_of_matches")

    def get(self, request, user_id, **kwargs):
        return self.list(request)


class GenericLuckyTicketView(GenericAPIView):
    serializer_class = LuckyTicketSerializer


class UserLuckyTicketsView(CreateModelMixin, ListModelMixin, GenericLuckyTicketView):
    permission_classes = [IsAuthenticated & ListOwnership]

    def initial(self, request, user_id, **kwargs):
        User = get_user_model()
        self.user = get_object_or_404(User.objects, pk=user_id)
        self.owners = {self.user}

        return super().initial(request, user_id, **kwargs)

    def get_queryset(self):
        return self.user.lucky_tickets.all()

    def post(self, request, user_id, **kwargs):
        request.data["user"] = user_id

        return self.create(request)

    def get(self, request, user_id, **kwargs):
        return self.list(request)


class LuckyTicketDetailView(UpdateModelMixin, DestroyModelMixin, GenericLuckyTicketView):
    queryset = LuckyTicket.objects
    permission_classes = [IsAuthenticated & ObjectOwnership]

    def patch(self, request, pk, **kwargs):
        return self.partial_update(request, pk=pk)

    def delete(self, request, pk, **kwargs):
        return self.destroy(request, pk=pk)
