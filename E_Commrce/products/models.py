from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import ActivatorModel
from category.models import Category
from customer.models import Business, Customer
from tag.models import TaggedItem


class Products(ActivatorModel):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=3, max_digits=10)
    category = models.ManyToManyField(Category, related_name='product')
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name="products", null=True, blank=True)
    business_user = models.ForeignKey(Business, on_delete=models.SET_NULL, related_name="product_user", default=None,
                                      null=True)
    slug = AutoSlugField(populate_from='name')
    brand = models.CharField(max_length=50)
    old_price = models.DecimalField(decimal_places=3, max_digits=10)
    new_price = models.DecimalField(decimal_places=3, max_digits=10)
    is_bestseller = models.BooleanField()
    is_featured = models.BooleanField()
    quantity = models.PositiveIntegerField()
    meta_keywords = models.CharField(max_length=50)
    meta_description = models.CharField(max_length=50)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    products_tags = GenericRelation(TaggedItem, related_query_name="products")
