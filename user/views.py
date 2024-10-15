from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer


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


    @action(["GET"], False, url_path=r"list")
    def getUsers(self, request) -> Response:
        querySet: QuerySet[User] = (
            self.get_queryset().all()
        )
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    @action(["GET"], False, url_path=r"(?P<pk>\w+)")
    def getUser(self, request, pk) -> Response:
        querySet: QuerySet[User] = (
            self.get_queryset()
            .filter(id=pk)
            .first()
        )
        serializer = self.get_serializer(querySet)
        return Response(serializer.data)