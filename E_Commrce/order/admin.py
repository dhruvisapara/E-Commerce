from django.contrib import admin
from order.models import Order, Points


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass



@admin.register(Points)
class PointsAdmin(admin.ModelAdmin):
    pass
