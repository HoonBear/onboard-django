import bcrypt
from rest_framework import serializers

from .models import User


def encrypt_password(raw_password) -> str:
    """비밀번호 암호화"""

    byte_password: bytes = raw_password.encode("utf-8")
    hashed_password: bytes = bcrypt.hashpw(byte_password, bcrypt.gensalt())

    return hashed_password.decode("utf-8")


def check_password(password: str, compare_password) -> bool:
    """비밀번호 값 체크"""

    return bcrypt.checkpw(password.encode("utf-8"), compare_password.encode("utf-8"))


class CreateUserSerializer(serializers.Serializer):

    loginId = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=4, write_only=True)
    name = serializers.CharField(max_length=50)

    def create(self, validated_data):

        encrypted_password = encrypt_password(validated_data["password"])

        user = User.objects.create(
            loginId=validated_data["loginId"],
            password=encrypted_password,
            name=validated_data["name"],
        )

        return user


class ListUserSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    createdAt = serializers.DateTimeField()


class RetrieveUserSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    loginId = serializers.CharField()
    name = serializers.CharField()
    createdAt = serializers.DateTimeField()
    modifiedAt = serializers.DateTimeField()
