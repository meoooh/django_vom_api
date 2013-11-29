from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *
from .forms import UserForm

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
    form = UserForm(request.DATA)

    if form.is_valid():
        user = VomUser.objects.create_user(
            email=form.cleaned_data['email'],
            name=form.cleaned_data['name'],
            birthday=form.cleaned_data['birthday'],
            sex=form.cleaned_data['sex'],
            password=form.cleaned_data['password'],
        )

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def changePassword(request, pk):
    pass
