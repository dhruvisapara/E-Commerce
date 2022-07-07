import pytest

from category.factories import CategoryFactory, SubCaegoryFactory
from category.models import Category


@pytest.fixture
def create_category(db) -> Category:
    request = CategoryFactory.create()
    return request


@pytest.fixture
def create_sub_category(db) -> Category:
    sub_category = SubCaegoryFactory.create()
    return sub_category
