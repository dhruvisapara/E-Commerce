import pytest
from pytest_factoryboy import register

from category.factories import CategoryFactory
from category.models import Category


def test_filter_category(db, create_category: Category):
    assert Category.objects.filter(categories="Book 1").exists()


def test_category_creation_using_factory(db):
    category = CategoryFactory(categories="flats", description="nknhkjk")
    assert category.categories == "flats"


def test_my_introduction(my_name):
    assert my_name == "I am Dhruvi"


@pytest.mark.skip
def test_full_name(full_name):
    assert full_name == "sapDhruvi"


register(CategoryFactory)


@pytest.mark.django_db
def test_category_factory_fixture(category_factory):

    return category_factory
