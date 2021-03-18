from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin

from .models import Draw
from .serializers import DrawSerializer


class GenericDrawView(GenericAPIView):
    queryset = Draw.objects
    serializer_class = DrawSerializer


class DrawListView(CreateModelMixin, GenericDrawView):
    def post(self, request):
        return self.create(request)
