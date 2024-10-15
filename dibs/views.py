from django.db import IntegrityError
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from dibs.models import DibsGroup, DibsDetail
from dibs.serializers import DibsGroupSerializer, DibsDetailSerializer
from product.models import Product
from user.models import User


# Create your views here.
class DibsGroupViewSet(viewsets.GenericViewSet):
    serializer_class = DibsGroupSerializer

    def get_queryset(self):
        queryset = DibsGroup.objects.all()
        return queryset

    @staticmethod
    def create(request, *args, **kwargs):
        userId = request.data["userId"]
        user = get_object_or_404(User, pk=userId)

        dibsGroup = DibsGroup.objects.create(
            name=request.data['name'],
            user=user,
        )

        return Response({"id": dibsGroup.id}, status=status.HTTP_201_CREATED)

    @staticmethod
    def destroy(request, pk: int) -> Response:
        dibsGroup = get_object_or_404(DibsGroup, id=pk)
        dibsGroup.delete()

        return Response(status=status.HTTP_200_OK)

    # @action(["GET"], False, url_path=r"list")
    def list(self, request) -> Response:
        querySet: QuerySet[DibsGroup] = (
            self.get_queryset()
        )
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    # @action(["GET"], True, url_path=r"detail")
    def retrieve(self, request, pk) -> Response:
        dibsGroup = get_object_or_404(DibsGroup, pk=pk)

        # Todo. 하위에 찜한 상품 나오게 하기

        serializer = self.get_serializer(dibsGroup)
        return Response(serializer.data)

class DibsDetailViewSet(viewsets.GenericViewSet):
    serializer_class = DibsDetailSerializer

    def get_queryset(self):
        queryset = DibsDetail.objects.all()
        return queryset

    @staticmethod
    def create(request, *args, **kwargs):
        dibsGroupId = request.data["dibsGroupId"]
        dibsGroup = get_object_or_404(DibsGroup, pk=dibsGroupId)

        productId = request.data["productId"]
        product = get_object_or_404(Product, pk=productId)

        try:
            dibsDetail = DibsDetail.objects.create(
                dibsGroup=dibsGroup,
                product=product,
            )
        except IntegrityError:
            return Response("duplicated", status=status.HTTP_400_BAD_REQUEST)

        return Response({"id": dibsDetail.id}, status=status.HTTP_201_CREATED)

    @staticmethod
    def destroy(request, pk: int) -> Response:
        dibsDetail = get_object_or_404(DibsDetail, id=pk)
        dibsDetail.delete()

        return Response(status=status.HTTP_200_OK)
