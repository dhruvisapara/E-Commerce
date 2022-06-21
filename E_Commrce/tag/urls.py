from rest_framework import routers

from tag.views import TagViewSet
from django.urls import include, path

router = routers.SimpleRouter()
router.register(r'tags', TagViewSet, basename="tags")
urlpatterns = [

    path('', include(router.urls))
]
