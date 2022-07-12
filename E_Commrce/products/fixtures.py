import pytest

from products.factories import ProductFactory
from products.models import Products


@pytest.fixture
def product_creation(db) -> Products:
    request = ProductFactory.create()
    return request

