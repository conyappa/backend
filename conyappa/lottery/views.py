from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from main.permissions import InternalCommunication, Ownership, ReadOnly
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Draw
from .serializers import DrawSerializer, TicketSerializer


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


class TicketPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 1000
    page_size_query_param = "page_size"


class GenericTicketView(GenericAPIView):
    serializer_class = TicketSerializer
    pagination_class = TicketPagination


class UserTicketsView(ListModelMixin, GenericTicketView):
    # Changing tickets is a feature we would like to have in the near future.
    # For now, and for security reasons, make this viewset read-only.
    permission_classes = [IsAuthenticated & Ownership & ReadOnly]

    def set_user(self, user_id):
        User = get_user_model()

        self.user = get_object_or_404(User.objects, pk=user_id)

    def get_queryset(self):
        return self.user.current_tickets

    def get(self, request, user_id):
        self.set_user(user_id)
        return self.list(request)
