import pytest
from customer.models import Customer
from rest_framework.test import APIClient


@pytest.fixture
def active_user(db) -> Customer:
    "It creates user A for test purposes."
    return Customer.objects.create_user(username="active-user", is_staff=True)


@pytest.fixture
def inactivate_user(db) -> Customer:
    "It creates user A for test purposes."
    return Customer.objects.create_user(username="inactive", is_staff=False)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user_B(db) -> Customer:
    """It creates user B."""
    return Customer.objects.create(username="abc")


@pytest.fixture
def client():
    return APIClient()
