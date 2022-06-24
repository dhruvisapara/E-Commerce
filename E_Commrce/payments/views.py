import stripe
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from order.models import Order
from order.serializer import OrderSerializer


class PymentViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        stripe.PaymentIntent.create(
            amount=1099,
            currency='inr',
            payment_method_types=['card']
        )
