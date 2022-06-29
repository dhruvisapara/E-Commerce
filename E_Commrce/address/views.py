from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from address.models import Address
from address.serializers import AddressSerializer
from pdb import set_trace as pdb


class UserAddress(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        """
            It should display all addresses of current user.
        """
        return self.queryset.filter(user_address=self.request.user)
