from rest_framework import serializers

from .models import SingleUser
from django.contrib.auth import authenticate

class UserSeriazlizer(serializers.Serializer):
    class Meta:
        model   = SingleUser
        fields=['ID']

class LoginUserSerializer(serializers.Serializer):
    ID          = serializers.CharField()
    password    = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")

