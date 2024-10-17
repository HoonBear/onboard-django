from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dibs.models import DibsDetail, DibsGroup
from dibs.paginator import DibsGroupPaginator
from dibs.serializers import CreateDibsGroupSerializer, \
    ListDibsGroupSerializer, RetrieveDibsGroupSerializer, CreateDibsDetailSerializer, RetrieveDibsDetailSerializer
from product.models import Product
from server.exceptions import AuthorizationException, DuplicatedDibsGroupNameException, DuplicatedDibsProduct


# Create your views here.
class DibsGroupViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = DibsGroupPaginator

    def get_serializer_class(self):
        if self.action == "create":
            return CreateDibsGroupSerializer
        if self.action == "list":
            return ListDibsGroupSerializer
        return RetrieveDibsGroupSerializer

    def get_queryset(self):
        queryset = DibsGroup.objects.prefetch_related("dibsDetails__product").all()
        return queryset

    def create(self, request, *args, **kwargs):
        # 찜 목록의 이름은 중복될 수 없다
        if DibsGroup.objects.filter(name=request.data["name"]).first() is not None:
            raise DuplicatedDibsGroupNameException

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(uesr=request.user)
        return Response({"id": instance.id}, status=status.HTTP_201_CREATED)

    def list(self, request) -> Response:
        # 요청 회원의 찜 목록만 가져온다
        querySet: QuerySet[DibsGroup] = self.get_queryset().filter(
            user__id=request.user.id
        )
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(querySet, request, view=self)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk) -> Response:
        dibsGroup = get_object_or_404(
            self.get_queryset().prefetch_related("dibsDetails__product"),
            id=pk,
        )

        # 로그인한 유저와 요청 찜 목록의 유저가 다르면 권한 없음
        if request.user.id != dibsGroup.user.id:
            raise AuthorizationException

        serializer = self.get_serializer(dibsGroup)
        return Response(serializer.data)

    @staticmethod
    def destroy(request, pk: int) -> Response:
        dibsGroup = get_object_or_404(DibsGroup, id=pk)

        # 로그인한 유저와 요청 찜 목록의 유저가 다르면 권한 없음
        if request.user.id != dibsGroup.user.id:
            raise AuthorizationException

        dibsGroup.delete()
        return Response(status=status.HTTP_200_OK)


class DibsDetailViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            return CreateDibsDetailSerializer
        return RetrieveDibsDetailSerializer

    def get_queryset(self):
        queryset = DibsDetail.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        dibsGroup = get_object_or_404(DibsGroup, pk=request.data["dibsGroupId"])

        if user.id != dibsGroup.user.id:
            raise AuthorizationException

        product = get_object_or_404(Product, pk=request.data["productId"])

        dibsDetail = (
            self.get_queryset()
            .filter(dibsGroup__user=user, product=product)
            .select_related("dibsGroup__user")
            .first()
        )

        if dibsDetail is not None:
            raise DuplicatedDibsProduct

        serializer = self.get_serializer(data=request.data, context={'dibsGroup': dibsGroup, 'product': product})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(uesr=user, product=product)
        return Response({"id": instance.id}, status=status.HTTP_201_CREATED)

    @staticmethod
    def destroy(request, pk: int) -> Response:
        dibsDetail = get_object_or_404(DibsDetail, id=pk)

        if request.user.id != dibsDetail.dibsGroup.user.id:
            raise AuthorizationException

        dibsDetail.delete()
        return Response(status=status.HTTP_200_OK)
