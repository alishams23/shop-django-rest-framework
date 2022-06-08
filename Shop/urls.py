
from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('retrieveProduct/<int:pk>/',Product_retrieve.as_view(),name="productsretrieve"),
    path('listProducts/',Products_list.as_view(),name="productslist"),
    path('searchlistview/',Searchlistview.as_view(),name="searchlistview"),
    path('createOrders/',Orders_create.as_view(),name="orderscreate"),
    path('deleteOrders/',Orders_delete.as_view(),name="Ordersdelete"),
    path('ordersList/',Orders_list.as_view(),name="Orderslist"),
    path('comment/<int:pk>/',Comment_create.as_view(),name="comment"),
    path('createOrder/<int:pk>/',Order_cerate.as_view(),name="deleteOrder"),
    path('deleteOrder/<int:pk>/',Order_delete.as_view(),name="deleteOrder"),
    path('order_remove/<int:pk>/',Order_remove.as_view(),name="order"),
    path('order_add/<int:pk>/',Order_add.as_view(),name="order"),
    path('category_retrieve/<int:pk>/',Category_retrieve.as_view(),name="category"),
    path('category_discount/',Discount_list.as_view(),name="discount"),
    path('Categories_api/',Categories_api.as_view(),name="discount"),
    path('Recent_products/',Recent_products.as_view(),name="Recent"),
    path('heder_image/',heder_image_list.as_view(),name="heder_image"),
    path('heder_corner_image/',heder_left_image_list.as_view(),name="heder_left_image"),
    path('main_page/',in_main_page.as_view(),name="in_main_page"),
    path('Category_main_api/',Category_main_api.as_view(),name="Category_main_api"),
    path('Stock_api/',Stock_api.as_view(),name="Stock_api"),
   
    path('cerate_Product_image/',cerate_Product_image.as_view(),name="cerate_Product_image"),
    path('UserCreate/',UserCreate.as_view(),name="UserCreate"),
    path('Code_check/',Code_check.as_view(),name="Code_check"),
    path('Send_code/',Send_code.as_view(),name="Send_code"),
    path('login/',obtain_auth_token),
    
]
