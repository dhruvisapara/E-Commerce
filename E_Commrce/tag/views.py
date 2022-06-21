from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from tag.models import TaggedItem
from tag.serializer import TagSerializer


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = TaggedItem.objects.all()
    authentication_classes = [JWTAuthentication]