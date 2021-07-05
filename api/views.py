from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import MyUser
from api.serizlizers import RegistrationUserSerializer, LoginUserSerializer


class RegistrationView(APIView):
    serializer_class = RegistrationUserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = MyUser(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    serializer_class = LoginUserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.data['email'], password=serializer.data['password'])
        if user is not None:
            login(request, user)
            token = Token.objects.get(user_id=user.id)
            return Response({"success": True, "token": token.key}, status=status.HTTP_200_OK)
        return Response({"success": False}, status=status.HTTP_418_IM_A_TEAPOT)