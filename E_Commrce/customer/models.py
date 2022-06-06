from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.constant import FEMALE, GENDER


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
    )  # Validators should be a list
    age = models.IntegerField(default=None, null=True, blank=True)

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
        return "%s %s" % (self.first_name, self.last_name)

    def isExists(self):
        """To check by email that user is existed or not"""
        if Customer.objects.filter(email=self.email):
            return True
        return False
