from django.db.models import QuerySet
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from server.exceptions import DuplicatedUserLoginIdException, AuthorizationException, IdOrPasswordNotFoundException
from server.authentication import JwtAuthentication
from user.models import User
from user.paginator import UserPaginator
from user.serializers import CreateUserSerializer, ReadUserSerializer, check_password


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    pagination_class = UserPaginator

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def list(self, request, *args, **kwargs) -> Response:
        querySet = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(querySet, request, view=self)
        serializer = ReadUserSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @staticmethod
    def retrieve(request, pk) -> Response:
        if request.user.id == int(pk):
            user = request.user
        else:
            raise AuthorizationException

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
            raise DuplicatedUserLoginIdException

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
            raise IdOrPasswordNotFoundException
        if not check_password(password, user.password):
            raise IdOrPasswordNotFoundException

        access_token = JwtAuthentication.issue_token(user.id)

        return Response(
            {"name": user.name, "access_token": access_token},
            status.HTTP_200_OK,
        )
