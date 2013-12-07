from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

@api_view(['POST'])
def createUser(request):
    """
    create user
    email -- A first parameter
    name -- A second parameter
    birthday -- A second parameter
    sex -- A second parameter
    password -- A second parameter
    password2 -- A second parameter
    """
    serializer = UserSerializer(data=request.DATA)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def changePassword(request, pk):
    pass
