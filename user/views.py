from django.db.models import QuerySet
from jwt import exceptions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from server.authentication import JwtAuthentication
from user.models import User
from user.serializers import CreateUserSerializer, ReadUserSerializer, check_password


class UserViewSet(viewsets.GenericViewSet):
    # serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    # @action(["GET"], False, url_path=r"list")
    def list(self, request) -> Response:
        querySet: QuerySet[User] = self.get_queryset()
        serializer = ReadUserSerializer(querySet, many=True)
        return Response(serializer.data)

    # @action(["GET"], True, url_path=r"detail")
    def retrieve(self, request, pk) -> Response:
        if request.user.id == int(pk):
            user = request.user  # 현재 로그인한 사용자 정보를 사용
        else:
            raise exceptions.InvalidTokenError

        serializer = ReadUserSerializer(user)
        return Response(serializer.data)

    @action(
        methods=["POST"], detail=False, url_path="signup", permission_classes=[AllowAny]
    )
    def signup(self, request) -> Response:
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User | None = User.objects.filter(
            loginId=request.data.get("loginId")
        ).first()

        if user:
            return Response("duplicated login id", status=status.HTTP_404_NOT_FOUND)

        instance = serializer.save()

        return Response({"id": instance.id}, status=status.HTTP_201_CREATED)

    @action(
        methods=["POST"], detail=False, url_path="login", permission_classes=[AllowAny]
    )
    def login(self, request) -> Response:
        loginId: str | None = request.data.get("loginId")
        password: str | None = request.data.get("password")

        user: User | None = User.objects.filter(loginId=loginId).first()

        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not check_password(password, user.password):
            return Response(status=status.HTTP_404_NOT_FOUND)

        access_token = JwtAuthentication.issue_token(user.id)

        return Response(
            {"name": user.name, "access_token": access_token},
            status.HTTP_200_OK,
        )
