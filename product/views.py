from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerializer


# Create your views here.
class ProductViewSet(viewsets.GenericViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        return Response({"id": instance.id}, status=status.HTTP_201_CREATED)

    @action(["GET"], False, url_path=r"list")
    def getProducts(self, request) -> Response:
        querySet: QuerySet[Product] = (
            self.get_queryset().all()
        )
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    @action(["GET"], False, url_path=r"(?P<pk>\w+)")
    def getUser(self, request, pk) -> Response:
        querySet: QuerySet[Product] = (
            self.get_queryset()
            .filter(id=pk)
            .first()
        )
        serializer = self.get_serializer(querySet)
        return Response(serializer.data)