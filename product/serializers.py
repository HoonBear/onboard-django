from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'thumbnail', 'price')

    name = serializers.CharField()
    thumbnail = serializers.CharField()
    price = serializers.IntegerField()

    def create(self, validated_data):
        product = Product.objects.create(
            name=validated_data['name'],
            thumbnail=validated_data['thumbnail'],
            price=validated_data['price'],
        )
        return product