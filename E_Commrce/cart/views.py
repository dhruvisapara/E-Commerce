from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartSerializer
from E_Commrce.mixin import CustomRenderer
from E_Commrce.permission import ModificationPermission
from order.models import Order


class CartView(ModelViewSet):
    """
        This viewset should create,update,retrieve and destroy by cart user only.
    """
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [ModificationPermission]
    renderer_classes = [CustomRenderer]

    def get_queryset(self) -> QuerySet:
        """
            This queryset should only display carts that are not ordered.
        """
        orders = Order.objects.all()
        cart_order = Cart.objects.exclude(cart_order__id__in=orders)
        return cart_order

    def get_renderer_context(self) -> dict:
        context = super().get_renderer_context()
        context['message'] = "hello"
        return context

    def list(self, request, *args, **kwargs) -> Response:
        page_size = self.request.query_params.get('page_size')
        if page_size:
            if page_size.lower() == 'all':
                self.pagination_class.page_size = len(self.queryset)

        response = super().list(self, request)
        if self.queryset.count() == 0:
            return Response({'message': "This Cart is empty."})
        return Response({'message': "successfully", 'result': response.data})


class CartItemAPIView(APIView):
    query_set = CartItem.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get(self, request, *args, **kwargs) -> Response:
        cart_items = self.query_set
        serializer = self.serializer_class(cart_items, many=True)
        return Response({"message": "cartitem successfully added.", "items": serializer.data})

    def post(self, request) -> Response:
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
