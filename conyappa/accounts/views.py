from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainSlidingView

from main.permissions import ListOwnership, ObjectOwnership

from .models import Device, User
from .serializers import DeviceSerializer, TokenLoginSerializer, UserSerializer


class TokenLoginView(TokenObtainSlidingView):
    serializer_class = TokenLoginSerializer


class GenericUserView(GenericAPIView):
    queryset = User.objects
    serializer_class = UserSerializer


class UserListView(CreateModelMixin, GenericUserView):
    def post(self, request, **kwargs):
        return self.create(request)


class UserDetailView(RetrieveModelMixin, UpdateModelMixin, GenericUserView):
    permission_classes = [IsAuthenticated & ObjectOwnership]

    def get(self, request, pk, **kwargs):
        return self.retrieve(request, pk=pk)

    def patch(self, request, pk, **kwargs):
        return self.partial_update(request, pk=pk)


class GenericDeviceView(GenericAPIView):
    serializer_class = DeviceSerializer


class UserDeviceListView(CreateModelMixin, UpdateModelMixin, GenericDeviceView):
    permission_classes = [IsAuthenticated & ListOwnership]

    def initial(self, request, user_id):
        self.user = get_object_or_404(User.objects, pk=user_id)
        self.owners = {self.user}

        return super().initial(request, user_id)

    def get_object(self):
        android_id = self.request.data.get("android_id")
        ios_id = self.request.data.get("ios_id")

        return Device.objects.get(android_id=android_id, ios_id=ios_id)

    def post(self, request, user_id, **kwargs):
        request.data["user"] = user_id

        try:
            return self.partial_update(request)
        except Device.DoesNotExist:
            return self.create(request)
