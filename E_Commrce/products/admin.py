from django.contrib import admin
from products.models import Products


@admin.register(Products)
class OrderAdmin(admin.ModelAdmin):
    pass
