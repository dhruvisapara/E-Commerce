import django_filters
from django_filters import rest_framework as filters, DateTimeFilter,  NumberFilter, UUIDFilter, Filter
from django_filters.rest_framework import FilterSet

from products.models import Products


class BrandFilter(filters.FilterSet):
    brand = django_filters.CharFilter(lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")
    is_bestseller = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Products
        fields = ["brand", "name", "is_bestseller", "is_active"]


class ProductFilter(FilterSet):
    """
        It should filter product by dates and prices.
    """
    from_manufacturing_date = DateTimeFilter(field_name='created_at',
                                             lookup_expr='gte')
    to_manufacturing_date = DateTimeFilter(field_name='updated_at',
                                           lookup_expr='lte')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')
    category_name = Filter(field_name="category__categories")
    user_name = Filter(field_name="user__username")

    class Meta:
        model = Products
        fields = (
            'name',
            'from_manufacturing_date',
            'to_manufacturing_date',
            'min_price',
            'max_price',
            'category_name',
            "user_name"
        )
