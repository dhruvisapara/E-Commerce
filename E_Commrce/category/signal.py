import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from category.models import Category


@receiver(pre_save, sender=Category)
def create_category(sender, instance, *args, **kwargs):
    instance.description = "In stock"
    return instance
