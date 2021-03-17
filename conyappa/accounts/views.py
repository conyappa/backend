from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
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
