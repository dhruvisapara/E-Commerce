from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from order.models import Order
from order.serializer import OrderSerializer
from utils.constant import PROCESSED


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    # queryset = Order.objects.filter(status=PROCESSED)
    queryset= Order.objects.all()
    authentication_classes = [JWTAuthentication]



