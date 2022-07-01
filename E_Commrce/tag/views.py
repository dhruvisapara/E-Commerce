from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from E_Commrce.mixxin import CustomRenderer
from E_Commrce.permission import StaffPermission
from tag.models import TaggedItem
from tag.serializers import TagSerializer


class TagViewSet(ModelViewSet):
    """
        This viewset is for create tags,update and delete tags by staff members only.
    """
    serializer_class = TagSerializer
    queryset = TaggedItem.objects.all()
    permission_classes = [StaffPermission]
    renderer_classes = CustomRenderer

