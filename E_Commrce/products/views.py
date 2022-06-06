from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from products.filter import BrandFilter
from products.models import Products
from products.serializer import ProductSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Products.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = BrandFilter
