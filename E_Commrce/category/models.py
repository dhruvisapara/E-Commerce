from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import ActivatorModel


class Category(ActivatorModel):
    category_name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='category_name')
    description = models.TextField()
    meta_keywords = models.CharField(max_length=50)
    meta_description = models.CharField(max_length=50)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,related_name="sub_category")

