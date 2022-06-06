import django_filters
from django_filters import rest_framework as filters
from category.models import Category


class Searchfilter(filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['name']
