from django.urls import path, include
from rest_framework import routers
from category.views import CategoryView

router = routers.SimpleRouter()
router.register(r'category', CategoryView, basename="category")


urlpatterns = [

    path('', include(router.urls)),
]
