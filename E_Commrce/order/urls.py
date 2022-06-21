from django.urls import include, path
from rest_framework import routers
from order.views import OrderViewSet


router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet, basename="orders")

urlpatterns = [

    path('', include(router.urls))
]
