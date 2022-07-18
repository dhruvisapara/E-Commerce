import pytest

from cart.factories import CartFactory, CartItemFactory
from cart.models import Cart, CartItem


@pytest.fixture
def cart_creation(db) -> Cart:
    """It should return  created factory data for cart model. """
    request = CartFactory.create()
    return request


@pytest.fixture
def cart_item_creation(db) -> CartItem:
    """It should return created factory data for cartitem model."""
    request = CartItemFactory.create()
    return request
@pytest.fixture
def update_cart_item(db) -> CartItem:
    request = CartItemFactory.create()
    return request
