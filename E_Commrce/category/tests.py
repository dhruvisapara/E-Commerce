from category.factories import CategoryFactory
from category.models import Category
from pdb import set_trace as pdb


def test_filter_category(db, create_category: Category):
    assert Category.objects.filter(categories="Book 1").exists()


def test_category_creation_using_factory(db):
    category = CategoryFactory(categories="flats", description="nknhkjk")
    assert category.categories == "flats"
