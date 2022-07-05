import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from products.factories import ProductFactory

register(ProductFactory)


@pytest.mark.django_db
def test_product_factory_fixture(product_factory):
    return product_factory
# def test_post_api():
