from django.db import models
from E_Commrce.settings import AUTH_USER_MODEL
from django.core.validators import RegexValidator


class Address(models.Model):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                "allowed.",
    )
    user_address = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_address",
                                     default=None, null=True, blank=True)
    phone = models.CharField(
        validators=[phone_regex], max_length=17, blank=True
    )
    email = models.EmailField()
    name = models.CharField(max_length=30, default=None)
    block = models.CharField(max_length=5, default=None)
    building_name = models.CharField(max_length=20, default=None)
    floor = models.CharField(max_length=20, null=True)
    flat_number = models.CharField(max_length=10, blank=True)
    street = models.CharField(max_length=20, default=1)
    area = models.CharField(max_length=20, default=None)

    @property
    def full_address(self):
        """Returns the customer's full address"""
        return "%s  %s  %s  %s  %s  %s  %s " % (
        self.name, self.flat_number, self.building_name, self.block, self.floor, self.street, self.area)
