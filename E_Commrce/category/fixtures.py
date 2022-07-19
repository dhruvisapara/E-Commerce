import pytest

from category.factories import CategoryFactory, SubCaegoryFactory
from category.models import Category


@pytest.fixture
def create_category(db) -> Category:
    """It should return  created factory data for category model."""
    request = CategoryFactory.create()
    return request


@pytest.fixture
def create_sub_category(db) -> Category:
    """It should return  created sub factory data for category model."""
    sub_category = SubCaegoryFactory.create()
    return sub_category
@pytest.fixture
def updated_fixture(db) -> Category:
    sub_category = SubCaegoryFactory.create()
    return sub_category

@pytest.fixture
def update_category(staff_user, db) -> Category:
    """It creates Category model data for update purpose."""
    updated = Category.objects.create(categories="cloth", description="ABCD", user=staff_user)
    return updated


@pytest.fixture
def update_sub_category(db) -> Category:
    """It creates Category model sub data for update purpose."""
    patched = Category.objects.create(categories="jeans", description="ABCD", user="dhruvi")
    return patched
