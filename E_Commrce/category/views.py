from rest_framework.viewsets import ModelViewSet

from category.models import Category
from category.serializers import CategorySerializer
from E_Commrce.permission import ModificationPermission, StaffPermission
from pdb import set_trace as pdb


class CategoryView(ModelViewSet):
    """
        Category will create here.
        Existing category should update ,destroy and retrieve by created user.
    """
    serializer_class = CategorySerializer
    permission_classes = [
        StaffPermission, ModificationPermission,

    ]
    queryset = Category.objects.all()

    filterset_fields = ["categories", "tags__tag"]
    search_fields = ["categories", "tags__tag"]
