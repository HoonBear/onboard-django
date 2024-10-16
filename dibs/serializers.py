from rest_framework import serializers

from product.serializers import ProductSerializer


class DibsDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    createdAt = serializers.DateTimeField
    modifiedAt = serializers.DateTimeField
    product = ProductSerializer(read_only=True)


class DibsGroupSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    createdAt = serializers.DateTimeField()
    modifiedAt = serializers.DateTimeField()
    dibsDetails = DibsDetailSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['dibsDetails'] = representation['dibsDetails'][:4]
        return representation
