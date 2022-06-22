from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from E_Commrce.permission import User_business_permission
from customer.models import Customer, Business
from customer.serializer import CustomerSerializer, BusinessUserSerializer, StaffMembersSerializer
from customer.task import send_email_task


class Registration(ViewSet, CreateModelMixin):
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    queryset = Customer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_email_task.delay()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )


class Userlist(ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return self.queryset.filter(username=self.request.user.username)


class BusinessViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = BusinessUserSerializer
    queryset = Business.objects.all()
    permission_classes = [
        User_business_permission
    ]

    def get_queryset(self):
        return self.queryset.filter(business_customer=self.request.user.id)


class RegisterStaffViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = StaffMembersSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser, ]

    def get_queryset(self):
        return self.queryset.filter(manager=self.request.user.id)


class StaffProfileViewSet(ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return self.queryset.filter(manager=self.request.user.id)
