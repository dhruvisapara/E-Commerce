from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from E_Commrce.permission import User_cart_permission
from cart.models import Cart, CartItem
from cart.serializer import CartItemSerializer, CartSerializer


class CartView(ModelViewSet):
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Cart.objects.all()
    permission_classes = [User_cart_permission]


class CartItemView(ModelViewSet):
    serializer_class = CartItemSerializer
    authentication_classes = [JWTAuthentication]
    queryset = CartItem.objects.all()
