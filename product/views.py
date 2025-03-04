from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from product.models import Product
from product.serializers import CreateProductSerializer, ListProductSerializer, RetrieveProductSerializer


# Create your views here.
class ProductViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]  # 모든 요청 허용

    def get_serializer_class(self):
        if self.action == "create":
            return CreateProductSerializer
        if self.action == "list":
            return ListProductSerializer
        return RetrieveProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        return Response({"id": instance.id}, status=status.HTTP_201_CREATED)

    def list(self, request) -> Response:
        querySet: QuerySet[Product] = self.get_queryset()
        serializer = self.get_serializer(querySet, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk) -> Response:
        product = get_object_or_404(Product, pk=pk)

        serializer = self.get_serializer(product)
        return Response(serializer.data)
