import pytest

from products.factories import ProductFactory
from products.models import Products


@pytest.fixture
def product_creation(db) -> Products:
    """It should return  created factory data for product model. """
    request = ProductFactory.create()
    return request

