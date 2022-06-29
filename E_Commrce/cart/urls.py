from django.urls import path, include
from rest_framework import routers
from cart.views import CartItemView, CartView

router = routers.SimpleRouter()
router.register(r'cart', CartView, basename="cart")
router.register(r'cart-item', CartItemView, basename="cart-item")

urlpatterns = [

    path('', include(router.urls))
]
