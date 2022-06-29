from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from customer.models import Business, Customer
from customer.serializers import (BusinessUserSerializer, CustomerSerializer,
                                  StaffMembersSerializer)
from customer.tasks import send_email_task
from E_Commrce.permission import UserBusinessPermission
from pdb import set_trace as pdb


class Registration(ViewSet, CreateModelMixin):
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    queryset = Customer.objects.all()
    #
    # def create(self, request, *args, **kwargs):
    #     serializer = CustomerSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     send_email_task.delay()
    #     return Response(
    #         serializer.data, status=status.HTTP_201_CREATED
    #     )


class Userlist(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """
            Only returns current user details.
        """
        return self.queryset.filter(username=self.request.user.username)


class BusinessViewSet(ModelViewSet):
    serializer_class = BusinessUserSerializer
    queryset = Business.objects.all()
    permission_classes = [
        UserBusinessPermission
    ]

    def get_queryset(self):
        """
            This queryset returns business registered by this user.
        """
        return self.queryset.filter(business_customer=self.request.user.id)


class RegisterStaffViewSet(ModelViewSet):
    serializer_class = StaffMembersSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser, ]

    def get_queryset(self):
        """
            It should display all staff user list created by current user.
        """
        return self.queryset.filter(manager=self.request.user.id)


class StaffProfileViewSet(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """
                    It should display all staff user list created by current user.
                """
        return self.queryset.filter(manager=self.request.user.id)
