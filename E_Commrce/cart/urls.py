from django.urls import path, include
from rest_framework import routers
from cart.views import  CartView,CartItemAPIView

router = routers.SimpleRouter()
router.register(r'cart', CartView, basename="cart")


urlpatterns = [

    path('', include(router.urls)),
    path('cart_item/',CartItemAPIView.as_view(),name="cart-item")
]
