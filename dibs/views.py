from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dibs.models import DibsDetail, DibsGroup
from dibs.serializers import DibsDetailSerializer, DibsGroupSerializer
from product.models import Product
from server.exceptions import AuthorizationException, DuplicatedDibsGroupNameException, DuplicatedDibsProduct


# Create your views here.
class DibsGroupViewSet(viewsets.GenericViewSet):
    serializer_class = DibsGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = DibsGroup.objects.prefetch_related("dibsDetails__product").all()
        return queryset

    @staticmethod
    def create(request, *args, **kwargs):
        if request.user.id:
            user = request.user
        else:
            raise AuthorizationException

        if DibsGroup.objects.filter(name=request.data["name"]).first() is not None:
            raise DuplicatedDibsGroupNameException

        dibsGroup = DibsGroup.objects.create(
            name=request.data["name"],
            user=user,
        )

        return Response({"id": dibsGroup.id}, status=status.HTTP_201_CREATED)

    @staticmethod
    def destroy(request, pk: int) -> Response:
        dibsGroup = get_object_or_404(DibsGroup, id=pk)

        if request.user.id != dibsGroup.user.id:
            raise AuthorizationException

        dibsGroup.delete()

        return Response(status=status.HTTP_200_OK)

    def list(self, request) -> Response:
        querySet: QuerySet[DibsGroup] = self.get_queryset().filter(
            user__id=request.user.id
        )

        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk) -> Response:
        dibsGroup = get_object_or_404(
            self.get_queryset().prefetch_related("dibsDetails__product"),
            id=pk,
        )

        if request.user.id != dibsGroup.user.id:
            raise AuthorizationException

        serializer = self.get_serializer(dibsGroup)
        return Response(serializer.data)


class DibsDetailViewSet(viewsets.GenericViewSet):
    serializer_class = DibsDetailSerializer

    def get_queryset(self):
        queryset = DibsDetail.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        dibsGroupId = request.data["dibsGroupId"]
        dibsGroup = get_object_or_404(DibsGroup, pk=dibsGroupId)

        if user.id != dibsGroup.user.id:
            raise AuthorizationException

        productId = request.data["productId"]
        product = get_object_or_404(Product, pk=productId)

        dibsDetail = (
            self.get_queryset()
            .filter(dibsGroup__user__id=user.id, product_id=productId)
            .select_related("dibsGroup__user")
            .first()
        )

        if dibsDetail is not None:
            raise DuplicatedDibsProduct

        dibsDetail = DibsDetail.objects.create(
            dibsGroup=dibsGroup,
            product=product,
        )

        return Response({"id": dibsDetail.id}, status=status.HTTP_201_CREATED)

    @staticmethod
    def destroy(request, pk: int) -> Response:
        dibsDetail = get_object_or_404(DibsDetail, id=pk)

        if request.user.id != dibsDetail.dibsGroup.user.id:
            raise AuthorizationException

        dibsDetail.delete()

        return Response(status=status.HTTP_200_OK)
