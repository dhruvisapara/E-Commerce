from django.db import models
from pdb import set_trace as pdb


class CustomManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('categories')
