from rest_framework import serializers

from food.models import Restorant, Like, Order


class RestorantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restorant
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('res', 'user', 'is_liked')
        extra_kwargs = {
            'user': {'read_only':True},
            'res': {'read_only': True},
            'is_liked': {'required':False}
        }

class OrderGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'status': {'read_only': True},
            'res': {'read_only': True},
        }


# class OrderPostSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Order
#         fields = '__all__'
#         extra_kwargs = {
#             'user': {'read_only': True},
#             'res': {'read_only': True},
#         }

