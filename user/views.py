from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer, check_password


# Create your views here.
# @api_view(['GET'])
# def getUsers(request):
#     users = User.objects.all()
#     serializer = GetUsersSerializer(users, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def getUser(request, pk):
#     user = User.objects.filter(id=pk).first()
#     serializer = GetUserSerializer(user)
#     return Response(serializer.data)

class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        return Response({"id": instance.id}, status=status.HTTP_201_CREATED)


    # @action(["GET"], False, url_path=r"list")
    def list(self, request) -> Response:
        querySet: QuerySet[User] = (
            self.get_queryset()
        )
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    # @action(["GET"], True, url_path=r"detail")
    def retrieve(self, request, pk) -> Response:
        user = get_object_or_404(User, pk=pk)

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, url_path="login")
    def login(self, request) -> Response:
        loginId: str | None = request.data.get("loginId")
        password: str | None = request.data.get("password")

        user: User | None = User.objects.filter(loginId=loginId).first()

        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not check_password(password, user.password):
            return Response(status=status.HTTP_404_NOT_FOUND)

        access_token = "Todo. token"

        return Response(
            {
                "name": user.name,
                "access_token": access_token
            },
            status.HTTP_200_OK,
        )