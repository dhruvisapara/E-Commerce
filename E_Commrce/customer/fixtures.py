import pytest
from customer.models import Customer
from rest_framework.test import APIClient


@pytest.fixture
def staff_user(db) -> Customer:
    """It creates user A for test purposes."""
    return Customer.objects.create_user(username="active-user", is_staff=True,password="staff1234##",is_superuser=True)


@pytest.fixture
def non_staff_user(db) -> Customer:
    """It creates user A for test purposes."""
    return Customer.objects.create_user(username="inactive", password="nonstaff1234##")


@pytest.fixture
def api_client():
    return APIClient()
