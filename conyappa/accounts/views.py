from main.permissions import Ownership
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainSlidingView

from .models import User
from .serializers import TokenLoginSerializer, UserSerializer


class TokenLoginView(TokenObtainSlidingView):
    serializer_class = TokenLoginSerializer


class GenericUserView(GenericAPIView):
    queryset = User.objects
    serializer_class = UserSerializer


class UserListView(CreateModelMixin, GenericUserView):
    def post(self, request):
        return self.create(request)


class UserDetailView(RetrieveModelMixin, UpdateModelMixin, GenericUserView):
    permission_classes = [IsAuthenticated & IsOwnerOfObject]

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def patch(self, request, pk):
        return self.partial_update(request, pk=pk)
