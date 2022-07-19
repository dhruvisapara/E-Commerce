import pytest

from address.factories import AddressFactory
from address.models import Address


@pytest.fixture
def address_creation(db) -> Address:
    """Here factory data is created for Address Model."""
    request = AddressFactory.create()
    return request
