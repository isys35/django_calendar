from rest_framework import serializers

from api.models import MyUser, UserEvent


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


class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ['title', 'start_event', 'end_event', 'notification']

    def to_internal_value(self, data):
        if data['end_event'] == '' and data['start_event']:
            data._mutable = True
            data['end_event'] = None
            data._mutable = False
        return super(EventUserSerializer, self).to_internal_value(data)
