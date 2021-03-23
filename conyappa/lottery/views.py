from logging import getLogger

from django.contrib.auth import get_user_model

from main.permissions import InternalCommunication, Ownership, ReadOnly
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from .models import Draw
from .serializers import DrawSerializer, TicketSerializer

logger = getLogger(__name__)


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


class OngoingUserTicketsView(ListModelMixin, GenericTicketView):
    # Changing tickets is a feature we would like to have in the near future.
    # For now, and for security reasons, make this viewset read-only.
    permission_classes = [IsAuthenticated & Ownership & ReadOnly]

    def dispatch(self, request, user_id):
        User = get_user_model()
        self.user = User.objects.get(pk=user_id)

        return super().dispatch(request)

    def get_queryset(self):
        return self.user.current_tickets

    def get(self, request):
        return self.list(request)
