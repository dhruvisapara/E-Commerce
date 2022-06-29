from django.contrib.contenttypes.fields import GenericRelation
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import ActivatorModel
from django.db import models

from E_Commrce.settings import AUTH_USER_MODEL
from category.manager import CustomManger
from tag.models import TaggedItem
from pdb import set_trace as pdb

class Category(ActivatorModel):
    categories = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from="categories")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, related_name="category_parent",null=True,blank=True)
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="sub_categories",
        default=None,

    )
    tags = GenericRelation(TaggedItem, related_query_name="tag_category")
    category = models.Manager()
    name = CustomManger()
