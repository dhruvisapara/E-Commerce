from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from E_Commrce.mixin import CustomRenderer
from E_Commrce.permission import ModificationPermission, StaffPermission
from products.filters import ProductFilter
from products.models import Products
from products.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [StaffPermission, ModificationPermission]
    filter_class = ProductFilter
    filterset_fields = ["brand", "name", "is_bestseller", "products_tags__tag", "category__categories",
                        "user__username"]
    search_fields = ["name", "brand", "category__categories", "user__username", "is_featured", "is_bestseller"]
    ordering_fields = ['name', 'brand', 'category__categories', 'user__username']
    # renderer_classes = [CustomRenderer]

    def perform_create(self, serializer) -> None:
        """
            For product registration user will be request user
        """
        serializer.save(user=self.request.user)

    def get_serializer(self, *args, **kwargs) -> Response:
        """
            To create and get list serializer data.
        """

        if "data" in kwargs:

            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(ProductViewSet, self).get_serializer(*args, **kwargs)
