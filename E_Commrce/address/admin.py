from django.contrib import admin

# Register your models here.
from address.models import Address


@admin.register(Address)
class Useraddress(admin.ModelAdmin):
    pass