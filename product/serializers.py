from rest_framework import serializers

from .models import Product


class CreateProductSerializer(serializers.Serializer):

    name = serializers.CharField()
    thumbnail = serializers.CharField()
    price = serializers.IntegerField()

    def create(self, validated_data):
        product = Product.objects.create(
            name=validated_data["name"],
            thumbnail=validated_data["thumbnail"],
            price=validated_data["price"],
        )
        return product

class ListProductSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    thumbnail = serializers.CharField()
    price = serializers.IntegerField()

class RetrieveProductSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.CharField()
    thumbnail = serializers.CharField()
    price = serializers.IntegerField()
    createdAt = serializers.DateTimeField()
    modifiedAt = serializers.DateTimeField()

class DibsDetailProductSerializer(serializers.Serializer):

    thumbnail = serializers.CharField()