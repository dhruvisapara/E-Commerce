import django_filters
from django_filters import rest_framework as filters
from products.models import Products


class BrandFilter(filters.FilterSet):

    brand = django_filters.CharFilter(lookup_expr="icontains")
    name = django_filters.CharFilter(lookup_expr="icontains")
    is_bestseller = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Products
        fields = ["brand", "name", "is_bestseller", "is_active"]
