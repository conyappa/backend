from main.permissions import InternalCommunication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from .fintoc import Interface as Fintoc


@api_view(["POST"])
@permission_classes([InternalCommunication])
def fetch_movements(request):
    Fintoc().fetch_movements()

    return Response(status=HTTP_204_NO_CONTENT)
