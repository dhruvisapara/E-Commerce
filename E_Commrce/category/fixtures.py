import pytest
from faker import Faker
from category.models import Category

faker = Faker()


@pytest.fixture
def create_category():
    """It should create category."""
    return Category.objects.create(categories="Book 1", description="ABC123")


@pytest.fixture
def me():
    return "Dhruvi"


@pytest.fixture
def my_name(me):
    return "I am " + me


@pytest.fixture
def full_name(me):
    return "sapara" + me
