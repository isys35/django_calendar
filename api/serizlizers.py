from rest_framework import serializers

from api.models import MyUser


class RegistrationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'password']
        write_only_fields = ['password']


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()

    class Meta:
        model = MyUser
        fields = ['email', 'password']
