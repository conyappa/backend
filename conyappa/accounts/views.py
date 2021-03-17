from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin

from .models import User
from .serializers import UserSerializer


class GenericUserView(GenericAPIView):
    queryset = User.objects
    serializer_class = UserSerializer


class UserListView(CreateModelMixin, GenericUserView):
    def post(self, request):
        return self.create(request)
