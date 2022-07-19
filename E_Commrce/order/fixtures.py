import pytest

from order.factories import OrderFactory
from order.models import Order


@pytest.fixture
def order_creation(db) -> Order:
    """Here factory data is created for Order model."""
    request = OrderFactory.create()
    return request
