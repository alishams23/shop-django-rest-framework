import imp
from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


class Image_serializers(serializers.ModelSerializer):
    class Meta:
        model=Image
        fields="__all__"



class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","id"]

    

class Comment_serializers(serializers.ModelSerializer):
    author = UserSerializers(required=False,read_only=True)
    class Meta:
        model=Comment
        fields="__all__"

class Order_serializers(serializers.ModelSerializer):
       class Meta:
        model=Order
        fields="__all__"


class heder_image_serializers(serializers.ModelSerializer):
    class Meta:
        model=heder_image
        fields="__all__"

class heder_left_image_serializers(serializers.ModelSerializer):
    class Meta:
        model=heder_left_image
        fields="__all__"

class UsersRegisterSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ("id",'username', 'password'
                  , 'first_name', 'last_name',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_password(self, validated_data):
        if len(validated_data) < 8:
            raise ValidationError("password need to be more than 8 character")
        return validated_data

    def validate_username(self, validated_data):
        username = validated_data
        special_characters = "!@#$%^&*()-+?=,<>/"
        if any(c in special_characters for c in username):
            raise ValidationError("Username must don't have character")
        return username.lower()

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields="__all__"


class Specification_serializer(serializers.ModelSerializer):

    class Meta:
        model=Specification
        fields="__all__"
        

        
class Product_serializers(serializers.ModelSerializer):
    def order_count_function(self, obj):
        user = None
        try:
            user = self.context.get("request").user
            dataOrder = Single_Order.objects.filter(author=user).order_by("-pk")
            if len(dataOrder) == 0 :
                return {"count":0}
            else :
                data = dataOrder[0].order.filter(product = obj.id)
                if len(data) == 0 :
                    return {"count":0}
                else :
                    return {"count":data[0].count}
        except:
            return {"count":0}

        
        
    order_count = serializers.SerializerMethodField("order_count_function")
    image = Image_serializers(many=True)
    comment=Comment_serializers(many=True)
    category= CategorySerializer(many=True)
    Specification=Specification_serializer(many=True)
    class Meta:
        model=Product
        fields="__all__"

        
class Orders_serializers(serializers.ModelSerializer):
    product = Product_serializers()
    class Meta:
        model=Order
        exclude=("author",)
        
        

        
class Single_orders_serializers(serializers.ModelSerializer):
    order = Orders_serializers(many=True)
    class Meta:
        model=Single_Order
        exclude=("author",)
        
        
        
