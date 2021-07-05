from rest_framework import serializers

from api.models import MyUser


class RegistrationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'password']

