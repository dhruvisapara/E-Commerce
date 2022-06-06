from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from E_Commrce.permission import StaffPermission
from category.filters import Searchfilter
from category.models import Category
from category.serializer import CategorySerializer


class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        StaffPermission,
    ]
    queryset = Category.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = Searchfilter


# class SubCategoryView(ModelViewSet):
#     serializer_class = SubCategorySerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [StaffPermission]
#     queryset = Category.objects.all()
#     filter_backends = (DjangoFilterBackend,)
#     filter_class = Searchfilter
