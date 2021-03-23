from main.permissions import InternalCommunication, ReadOnly
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from .models import Draw
from .serializers import DrawSerializer


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
