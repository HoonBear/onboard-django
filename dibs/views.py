from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from dibs.models import DibsGroup
from dibs.serializers import DibsGroupSerializer
from user.models import User


# Create your views here.
class DibsGroupViewSet(viewsets.GenericViewSet):
    serializer_class = DibsGroupSerializer

    def get_queryset(self):
        queryset = DibsGroup.objects.all()
        return queryset

    @staticmethod
    def create(request, *args, **kwargs):
        user_id = request.data["userId"]
        user = get_object_or_404(User, pk=user_id)

        dibs_group = DibsGroup.objects.create(
            name=request.data['name'],
            user=user,
        )

        return Response({"id": dibs_group.id}, status=status.HTTP_201_CREATED)

    @action(["GET"], False, url_path=r"list")
    def getDibsGroups(self, request) -> Response:
        querySet: QuerySet[DibsGroup] = (
            self.get_queryset()
        )
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    @action(["GET"], True, url_path=r"detail")
    def getDibsGroup(self, request, pk) -> Response:
        dibsGroup = get_object_or_404(DibsGroup, pk=pk)

        serializer = self.get_serializer(dibsGroup)
        return Response(serializer.data)