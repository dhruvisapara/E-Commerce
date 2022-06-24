import stripe
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from order.models import Order
from order.serializer import OrderSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        try:
            response = stripe.Charge.create(
                amount=product.price,
                currency="usd",
                source=request.data["token"],  # Done with Stripe.js
                description="Product"
            )
            product.charge_id = response.charge_id
        except:
            return "done"
