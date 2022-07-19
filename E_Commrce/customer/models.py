from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from category.manager import CustomManger
from utils.constant import (
    FEMALE,
    GENDER,
    BUISNESS_TYPE,
    B2B_COMPANIES
)
from pdb import set_trace as pdb


class Customer(AbstractUser):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                "allowed.",
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(default=FEMALE, choices=GENDER, max_length=8)
    address = models.TextField(blank=True)
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True
    )
    age = models.IntegerField(default=None, null=True, blank=True)
    manager = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="staff_members",
        default=None,

    )

    # def get_age(self):
    #     """Count the Customer's age from birth_date"""
    #     user_age = date.today() - self.birth_date
    #     return int(user_age.days / 365.25)
    #
    # def save(self, *args, **kwargs):
    #     """Returns the customer's age."""
    #     self.age = self.get_age()
    #     super(Customer, self).save(*args, **kwargs)

    @property
    def full_name(self):
        """Returns the customer's full name."""
        return "{first_name}, {last_name}".format(first_name=self.first_name,
                                                  last_name=self.last_name,
                                                  )


class Business(models.Model):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                "allowed.",
    )
    business_customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        default=None,
        related_name="company",
        blank=True,
        null=True,
    )
    company_name = models.CharField(max_length=20)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    company_email = models.EmailField(_("email address"), blank=True)
    Nature_of_business = models.CharField(
        default=B2B_COMPANIES, choices=BUISNESS_TYPE, max_length=15
    )
    Year_of_Establishment = models.DateField()
    number_of_employees = models.IntegerField(default=4)
    product_category = models.CharField(max_length=10)
    revenue = models.DecimalField(decimal_places=3, max_digits=20)
    offline_channel = models.BooleanField()
    company_profile = models.TextField()
    portfolio = models.IntegerField()
    objects = models.Manager()

