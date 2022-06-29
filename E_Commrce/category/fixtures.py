import pytest
from faker import Faker
from category.models import Category
from pdb import set_trace as pdb

faker = Faker()


@pytest.fixture
def create_category():
    """It should create category."""
    return Category.objects.create(categories="Book 1", description="ABC123")
