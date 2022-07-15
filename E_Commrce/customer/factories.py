import random

from factory.django import DjangoModelFactory
import factory

from customer.models import Customer, Business
from utils.constant import GENDER, BUISNESS_TYPE


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    username = factory.Faker("name")
    email = 'dhruvi.sapara@trootech.com'
    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    password = 'setpassword1234'
    birth_date = factory.Faker("date")
    gender = random.choice([x[1] for x in GENDER])
    address = factory.Faker("name")
    age = factory.Faker("random_number")
    phone_number = factory.Faker("random_number")
    is_staff = True
    is_superuser = True


class BusinessFactory(DjangoModelFactory):
    class Meta:
        model = Business

    company_name = factory.Faker("name")
    phone_number = factory.Faker("random_number")
    company_email = 'trootech@gmail.com'
    Nature_of_business = random.choice([x[1] for x in BUISNESS_TYPE])
    Year_of_Establishment = factory.Faker("date")
    number_of_employees = factory.Faker('random_number')
    product_category = factory.Faker("name")
    revenue = factory.Faker('pyint', min_value=0, max_value=1000000)
    offline_channel = factory.Faker("pybool")
    company_profile = factory.Faker("name")
    portfolio = factory.Faker('random_number')
    business_customer = factory.SubFactory(CustomerFactory)
