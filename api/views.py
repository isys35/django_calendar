from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import MyUser
from api.serizlizers import RegistrationUserSerializer


class RegistrationView(APIView):
    serializer_class = RegistrationUserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = MyUser.objects.create(email=request.data['email'])
        user.set_password(request.data['password'])
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)
