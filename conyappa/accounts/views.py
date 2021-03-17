from rest_framework_simplejwt.views import TokenObtainSlidingView

from .serializers import TokenLoginSerializer


class TokenLoginView(TokenObtainSlidingView):
    serializer_class = TokenLoginSerializer
