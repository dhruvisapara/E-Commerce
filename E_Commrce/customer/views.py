from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from customer.models import Customer
from customer.serializer import CustomerSerializer


class Registration(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    queryset = Customer.objects.all()


class Userlist(ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.queryset.filter(username=self.request.user.username)
        return user
