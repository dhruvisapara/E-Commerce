from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from E_Commrce.permission import ModificationPermission
from order.models import Order
from pdb import set_trace as pdb

ViewSet
class CartView(ModelViewSet):
    """
        This viewset should create,update,retrieve and destroy by cart user only.
    """
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [ModificationPermission]

    def get_queryset(self):
        """
            This queryset should only display carts that are not ordered.
        """
        orders = Order.objects.all()
        cart_order = Cart.objects.exclude(cart_order__id__in=orders)
        return cart_order


class CartItemView(ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
