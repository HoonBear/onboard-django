from rest_framework import serializers

from dibs.models import DibsGroup, DibsDetail
from product.serializers import DibsDetailProductSerializer, RetrieveProductSerializer


class CreateDibsDetailSerializer(serializers.Serializer):

    dibsGroup = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        return DibsDetail.objects.create(
            dibsGroup=self.context.get('dibsGroup'),
            product=self.context.get('product'),
        )

class RetrieveDibsDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    createdAt = serializers.DateTimeField
    modifiedAt = serializers.DateTimeField
    product = DibsDetailProductSerializer(read_only=True)

class RetrieveDibsProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    createdAt = serializers.DateTimeField
    modifiedAt = serializers.DateTimeField
    product = RetrieveProductSerializer(read_only=True)

class CreateDibsGroupSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=20)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        return DibsGroup.objects.create(
            name=validated_data["name"],
            user=self.context["request"].user,
        )

class ListDibsGroupSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    dibsDetails = RetrieveDibsDetailSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['dibsDetails'] = representation['dibsDetails'][:4]
        return representation

class RetrieveDibsGroupSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    createdAt = serializers.DateTimeField()
    modifiedAt = serializers.DateTimeField()
    dibsDetails = RetrieveDibsProductDetailSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['dibsDetails'] = representation['dibsDetails'][:4]
        return representation
