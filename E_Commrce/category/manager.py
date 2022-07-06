from django.db import models


class CustomManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(categories__icontains="top")
