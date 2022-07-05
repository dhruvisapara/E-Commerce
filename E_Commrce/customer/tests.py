import pytest
from pytest_factoryboy import register

from customer.factories import CustomerFactory
from customer.models import Customer


def test_should_check_password(db, user_A: Customer) -> None:
    user_A.set_password("secret")
    assert user_A.check_password("secret") is True


def test_should_not_check_unusable_password(db, user_A: Customer) -> None:
    user_A.set_password("secret")
    user_A.set_unusable_password()
    assert user_A.check_password("secret") is False


def test_customer_exists_or_not(db, user_B: Customer):
    assert Customer.objects.filter(username="B").exists() is False


register(CustomerFactory)


@pytest.mark.django_db
def test_customer_factory_fixture(customer_factory):
    return customer_factory


class TestUserViewSet:
    endpoint = '/user/'

    def test_list(self, client):
        client.force_authenticate(user=client)
        response = client.get(self.endpoint)
        return response
