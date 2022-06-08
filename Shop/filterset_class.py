
from django_filters import rest_framework as filtersS  
from .models import Product


class Price_filter(filtersS.FilterSet):
    min_price = filtersS.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filtersS.NumberFilter(field_name="price", lookup_expr='lte')
    min_discount = filtersS.NumberFilter(field_name="discount", lookup_expr='gte')
    min_amount = filtersS.NumberFilter(field_name="amount", lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price',"category","min_amount","min_discount","is_stock","is_people"]