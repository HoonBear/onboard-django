from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):

    loginId = serializers.CharField()
    password = serializers.CharField()
    name = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create(
            loginId=validated_data['loginId'],
            password=validated_data['password'],
            name=validated_data['name'],
        )
        return user