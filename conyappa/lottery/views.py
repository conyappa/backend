import threading as th

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from accounts.models import Device
from main.permissions import InternalCommunication, ListOwnership, ReadOnly
from main.versioning import VersionedView

from .models import Draw
from .pagination import TicketPagination
from .serializers import DrawSerializer, PrizeField, TicketSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def draws_metadata(request):
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
def choose_result(request):
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


class GenericDrawView(GenericAPIView, VersionedView):
    queryset = Draw.objects
    serializer_class = DrawSerializer


class DrawListView(CreateModelMixin, GenericDrawView):
    permission_classes = [InternalCommunication]

    def post(self, request):
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

    def get(self, request):
        return self.retrieve(request)


class GenericTicketView(GenericAPIView, VersionedView):
    serializer_class = TicketSerializer
    pagination_class = TicketPagination


class UserTicketsView(ListModelMixin, GenericTicketView):
    # Changing tickets is a feature we would like to have in the near future.
    # For now, and for security reasons, make this viewset read-only.
    permission_classes = [IsAuthenticated & ListOwnership & ReadOnly]

    def initial(self, request, user_id):
        User = get_user_model()
        self.user = get_object_or_404(User.objects, pk=user_id)
        self.owners = {self.user}

        return super().initial(request, user_id)

    def get_queryset(self):
        return self.user.current_tickets.order_by("-number_of_matches")

    def get(self, request, user_id):
        return self.list(request)
