from django.contrib.contenttypes.fields import GenericRelation
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import ActivatorModel
from django.db import models
from tag.models import TaggedItem


class Category(ActivatorModel):
    categories = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = AutoSlugField(populate_from="categories")
    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="sub_categories",
        default=None,

    )
    tags = GenericRelation(TaggedItem, related_query_name="category")
    category = models.Manager()




