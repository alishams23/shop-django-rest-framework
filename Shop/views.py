
import random
from django.db.models.query import QuerySet
from rest_framework import filters
from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import CreateAPIView, views
from django_filters import rest_framework as filterSpecial

from Shop.filterset_class import Price_filter
from .models import Order, Product
from .Serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .pagination import *
from rest_framework.authtoken.models import Token
import time
import requests
import json


class Code_check(APIView):
    def get(self, request):
        code = self.request.GET['code']
        if str(request.user.verify_phone_code) == str(code):
            userInstance = request.user
            userInstance.verify_phone = True
            userInstance.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class Send_code(APIView):
    def get(self, request):
        if request.user.count_sms < 10:
            userInstance = request.user
            userInstance.verify_phone_code = random.randint(10000, 99999)
            userInstance.save()
            try:
                newURL = 'https://console.melipayamak.com/api/send/shared/1806bb276635474486b7c380b2b0fbcb'
                newHeaders = {
                    'Content-type': 'application/json; utf-8', 'Accept': 'application/json'}
                newBody = {
                    "bodyId": 77293,
                    "to": f"{request.user.username}",
                    "args": [f"{request.user.verify_phone_code}"],
                }
                response = requests.post(
                    newURL, data=json.dumps(newBody), headers=newHeaders)
                print(response.json())
                userInstance = request.user
                userInstance.count_sms += 1
                userInstance.save()
                return Response({"result": response.json()}, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_410_GONE)


class Product_retrieve(RetrieveAPIView):
    serializer_class = Product_serializers
    queryset = Product.objects.filter(hide=False)


class Products_list(ListAPIView):
    serializer_class = Product_serializers
    queryset = Product.objects.filter(hide=False)
    pagination_class = SetPaginationOne


class Orders_create(CreateAPIView):
    serializer_class = Orders_serializers
    queryset = Order.objects.all()
    permissions_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(auther=self.request.user)


class Orders_delete(DestroyAPIView):
    serializer_class = Orders_serializers
    queryset = Order.objects.all()
    permissions_class = [IsAuthenticated]


class Orders_list(ListAPIView):
    serializer_class = Single_orders_serializers
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Single_Order.objects.filter(author=self.request.user).order_by("-pk")


class Order_Retrieve(RetrieveAPIView):
    # lookup_field = "pk"
    serializer_class = Orders_serializers

    permissions_classes = [IsAuthenticated, ]

    def get_queryset(self):

        return Order.objects.all()


class Comment_create(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = Comment_serializers

    def perform_create(self, serializer):
        id = self.kwargs.get('pk', 'Default Value if not there')
        data = serializer.save(author=self.request.user)
        instanceProduct = Product.objects.get(pk=id)
        instanceProduct.comment.add(data)


class Order_add(APIView):
    permissions_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        dataOrder = Single_Order.objects.filter(author=request.user).order_by("-pk")
        if len(dataOrder) == 0  :
            dataOrder = Single_Order.objects.create(author=request.user)
        else:
            dataOrder = dataOrder[0]
        id = kwargs.get('pk', 'Default Value if not there')
        dataProduct = Product.objects.get(id=id)
        data = dataOrder.order.filter(product = dataProduct)
        if len(data) != 0 :
            data = data[0]
            data.count += 1
            data.save()
        else:
            orderCreated = Order.objects.create(author=request.user,product=dataProduct)
            dataOrder.order.add(orderCreated)
        

        return Response(status=status.HTTP_200_OK)


class Order_remove(APIView):
    permissions_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        dataOrder = Single_Order.objects.filter(author=request.user).order_by("-pk")[0]
        id = kwargs.get('pk', 'Default Value if not there')
        dataProduct = Product.objects.get(id=id)
        data = dataOrder.order.filter(product = dataProduct)[0]
        if data.count == 1:
            data = dataOrder.order.remove(data)
        else:
            data.count -= 1
            data.save()

        return Response(status=status.HTTP_200_OK)




class cerate_Product_image(CreateAPIView):
    serializer_class = Image_serializers
    queryset = Image.objects.all()
    permissions_classes = [IsAuthenticated, ]
    
    def perform_create(self, serializer):
        data = serializer.save(author=self.request.user)
        
        
class Order_cerate(CreateAPIView):
    serializer_class = Order_serializers
    queryset = Order.objects.all()
    permissions_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        id = self.kwargs.get('pk', 'Default Value if not there')
        data = serializer.save(author=self.request.user)
        instanceProduct = Order.objects.get(pk=id)
        instanceProduct.order.add(data)


class Order_delete(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = Order_serializers
    permissions_classes = [IsAuthenticated, ]


class Searchlistview(generics.ListAPIView):
    queryset = Product.objects.filter(hide=False)
    serializer_class = Product_serializers
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, filterSpecial.DjangoFilterBackend]
    pagination_class = SetPaginationOne
    filterset_class = Price_filter
    ordering = ["-pk"]

    search_fields = ['title', ]


class Category_retrieve(ListAPIView):
    serializer_class = Product_serializers

    def get_queryset(self):
        id = self.kwargs.get('pk', 'Default Value if not there')
        data = Product.objects.filter(category__pk=id,hide=False)
        return data
    pagination_class = SetPaginationOne


class Discount_list(ListAPIView):
    serializer_class = Product_serializers

    def get_queryset(self):
        return Product.objects.filter(discount__range=["1", "100"])
    pagination_class = SetPaginationOne
    ordering = ["-discount"]


class Recent_products(ListAPIView):
    serializer_class = Product_serializers

    def get_queryset(self):
        return Product.objects.filter(hide=False).order_by("-pk")[0:10]


class heder_image_list(ListAPIView):
    queryset = heder_image.objects.all()
    serializer_class = heder_image_serializers


class heder_left_image_list(ListAPIView):
    queryset = heder_left_image.objects.all()
    serializer_class = heder_left_image_serializers


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersRegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, created = Token.objects.get_or_create(
            user_id=response.data["id"])
        response.data["token"] = str(token)
        return response


class in_main_page(ListAPIView):
    queryset = Category.objects.filter(is_main_page=True,hide=False)
    serializer_class = CategorySerializer


class Categories_api(ListAPIView):
    queryset = Category.objects.filter(hide=False)
    serializer_class = CategorySerializer


class Category_main_api(ListAPIView):
    queryset = Category.objects.filter(hide=False)
    serializer_class = CategorySerializer


class Stock_api(ListAPIView):
    queryset = Product.objects.filter(is_stock=True)
    serializer_class = Product_serializers
    pagination_class = SetPaginationOne
