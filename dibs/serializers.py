from rest_framework import serializers

from .models import DibsGroup, DibsDetail


class DibsGroupSerializer(serializers.Serializer):
    class Meta:
        model = DibsGroup
        fields = ('id', 'name', 'createdAt', 'modifiedAt', 'user')

    id = serializers.IntegerField()
    name = serializers.CharField()
    createdAt = serializers.DateTimeField()
    modifiedAt = serializers.DateTimeField()
    get_user = serializers.SerializerMethodField

    # def create(self, validated_data):
    #     dibsGroup = DibsGroup.objects.create(
    #         name=validated_data['name'],
    #         user=validated_data['user'],
    #     )
    #     return dibsGroup

class DibsDetailSerializer(serializers.Serializer):
    class Meta:
        model = DibsDetail
        fields = ('id', 'dibsGroup', 'product', 'createdAt', 'modifiedAt')

        id = serializers.IntegerField()
        get_dibs_group = serializers.SerializerMethodField
        get_product = serializers.SerializerMethodField
        createdAt = serializers.DateTimeField
        modifiedAt = serializers.DateTimeField
