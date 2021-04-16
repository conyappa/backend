from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from main.permissions import InternalCommunication, ListOwnership, ReadOnly

from .models import Draw
from .pagination import TicketPagination
from .serializers import DrawSerializer, TicketSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def metadata(request):
    prizes = {str(i): value for (i, value) in enumerate(settings.PRIZES)}

    return Response(
        data={
            "prizes": prizes,
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

    return Response(data=serializer.data, status=HTTP_200_OK)


class GenericDrawView(GenericAPIView):
    queryset = Draw.objects
    serializer_class = DrawSerializer


class DrawListView(CreateModelMixin, GenericDrawView):
    permission_classes = [InternalCommunication]

    def post(self, request):
        return self.create(request)


class OngoingDrawView(RetrieveModelMixin, GenericDrawView):
    permission_classes = [IsAuthenticated & ReadOnly]

    def get_object(self):
        return Draw.objects.ongoing()

    def get(self, request):
        return self.retrieve(request)


class GenericTicketView(GenericAPIView):
    serializer_class = TicketSerializer
    pagination_class = TicketPagination


class UserTicketsView(ListModelMixin, GenericTicketView):
    # Changing tickets is a feature we would like to have in the near future.
    # For now, and for security reasons, make this viewset read-only.
    permission_classes = [IsAuthenticated & ListOwnership & ReadOnly]

    def initial(self, request, user_id):
        User = get_user_model()
        self.owner = get_object_or_404(User.objects, pk=user_id)
        return super().initial(request, user_id)

    def get_queryset(self):
        return self.owner.current_tickets.order_by("-number_of_matches")

    def get(self, request, user_id):
        return self.list(request)
