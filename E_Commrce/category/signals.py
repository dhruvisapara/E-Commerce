from django.db.models.signals import pre_save
from django.dispatch import receiver
from category.models import Category
from pdb import set_trace as pdb


@receiver(pre_save, sender=Category)
def create_category(sender, instance, *args, **kwargs):
    """
        This signal will call after category was created and make description "in stock"
    """
    instance.description = "In stock"
    return instance
