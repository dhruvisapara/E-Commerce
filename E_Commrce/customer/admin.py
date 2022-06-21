from django.contrib import admin
from customer.models import Customer, Business


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Business)
class BuisnessUser(admin.ModelAdmin):
    pass
