import pytest
from rest_framework.reverse import reverse
from customer.models import Customer
from pdb import set_trace as pdb
from rest_framework.test import APIClient


@pytest.fixture
def user_A(db) -> Customer:
    "It creates user A for test purposes."
    return Customer.objects.create_user("A")


@pytest.fixture
def user_B(db) -> Customer:
    """It creates user B."""
    return Customer.objects.create(username="abc")


@pytest.fixture
def client():
    return APIClient()
