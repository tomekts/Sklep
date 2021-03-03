from django.contrib.auth.models import User, Group
from .models import Products, Category, Producer, CartProducts, Cart, User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','url', 'username', 'email', 'groups', 'password', 'last_name']


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'url', 'category', 'producer', 'title', 'description', 'price', 'image']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']


class ProducerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Producer
        fields = ['name', 'description', 'image']


class CartProductsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CartProducts
        fields = ['CartId', 'ProductsId', 'Count']


class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cart
        fields = ['url', 'UserId']