from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginUserSerializer(serializers.Serializer):
    ID = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
