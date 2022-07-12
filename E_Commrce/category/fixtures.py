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


@pytest.fixture
def update_category(staff_user, db) -> Category:
    updated = Category.objects.create(categories="cloth", description="ABCD", user=staff_user)
    return updated


@pytest.fixture
def update_sub_category(db) -> Category:
    patched = Category.objects.create(categories="jeans", description="ABCD", user="dhruvi")
    return patched


