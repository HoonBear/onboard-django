from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import DibsGroup, DibsDetail

class DibsDetailSerializer(serializers.Serializer):
    # class Meta:
    #     model = DibsDetail
    #     fields = ('id', 'createdAt', 'modifiedAt')

    id = serializers.IntegerField()
    createdAt = serializers.DateTimeField
    modifiedAt = serializers.DateTimeField
    product = ProductSerializer(read_only=True)


class DibsGroupSerializer(serializers.Serializer):

    # class Meta:
    #     model = DibsGroup
    #     fields = ('id', 'name', 'createdAt', 'modifiedAt', 'dibsDetails')

    id = serializers.IntegerField()
    name = serializers.CharField()
    createdAt = serializers.DateTimeField()
    modifiedAt = serializers.DateTimeField()
    dibsDetails = DibsDetailSerializer(many=True, read_only=True)
