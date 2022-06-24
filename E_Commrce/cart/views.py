from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from E_Commrce.permission import Modification_permission
from cart.models import Cart, CartItem
from cart.serializer import CartItemSerializer, CartSerializer
from order.models import Order


class CartView(ModelViewSet):
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Cart.objects.all()
    permission_classes = [Modification_permission]

    def get_queryset(self):
        orders = Order.objects.all()
        cart_order = Cart.objects.exclude(cart_order__id__in=orders)
        return cart_order


class CartItemView(ModelViewSet):
    serializer_class = CartItemSerializer
    authentication_classes = [JWTAuthentication]
    queryset = CartItem.objects.all()
