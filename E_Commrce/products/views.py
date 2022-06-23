from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from E_Commrce.permission import Modification_permission, StaffPermission
from products.filter import BrandFilter
from products.models import Products
from products.serializer import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = (DjangoFilterBackend,)
    filter_class = BrandFilter
    permission_classes = [StaffPermission, Modification_permission]

    def perform_create(self, serializer):
        """For product registration user will be request user"""
        serializer.save(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:

            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(ProductViewSet, self).get_serializer(*args, **kwargs)
