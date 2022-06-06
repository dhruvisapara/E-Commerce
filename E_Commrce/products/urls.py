from django.urls import include, path
from rest_framework import routers
from products.views import ProductViewSet

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet, basename="products")

urlpatterns = [

    path('', include(router.urls))
]
