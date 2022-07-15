from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_204_NO_CONTENT,
)
from rest_framework.test import APITestCase

from customer.factories import CustomerFactory
from customer.models import Customer, Business

TOKEN_URL = "/api/v1/get_token/"
BASE_URL = "/api/v1/register/"
BUSINESS_USER_URL = "/api/v1/business_register/"
STAFF_REGISTRATION = "/api/v1/staff_register/"
STAFF_LIST = "/api/v1/staff_list/"
BUSINESS_USER_PAYLOAD = dict()
STAFF_USER_PAYLOAD = dict()
DELETE_USER_PAYLOAD = dict()
DELETE_COUNT = 0


class RegisterUserTest(APITestCase):
    username = "django"
    password = "1234pass"
    password2 = "1234pass"
    first_name = "good"
    last_name = "luck"
    email = "dhruvi@trootech.com"

    def setUp(self):
        self.user = Customer.objects.create_user(
            username=self.username,
            password=self.password,
            first_name=self.first_name,
            email=self.email,
            last_name=self.last_name,
        )

    def test_successful_registration_gives_201(self):
        data = {
            "username": "hello",
            "password": self.password,
            "password2": self.password2,
            "email": "hello@gmail.com",
            "first_name": self.first_name,
            "last_name": self.last_name,
        }
        empty_customer_data = Customer.objects.all().count()
        response = self.client.post(BASE_URL, data)
        created_customer = Customer.objects.all().count()
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(created_customer, empty_customer_data + 1)


class LoginUserTest(APITestCase):
    username = "someuser"
    password = "1234pass"

    def setUp(self):
        self.user = Customer.objects.create_user(
            username=self.username, password=self.password
        )

    def test_successful_login_gives_200(self):
        response = self.client.post(
            TOKEN_URL,
            {"username": self.username, "password": self.password},
            format="json",
        )
        assert response.status_code == HTTP_200_OK


class FailLoginTest(APITestCase):
    def setUp(self):
        self.user = CustomerFactory.create()
        self.jwt_url = TOKEN_URL

    def test_post_form_failing_jwt_auth(self):
        """
        Ensure POSTing form over JWT auth without correct credentials fails
        """

        data = {"username": self.user.username, "password": "inCorrect01"}
        response = self.client.post(self.jwt_url, data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)


class DeleteUserTest(APITestCase):
    username = "hello"
    password = "1234pass"
    password2 = "1234pass"
    first_name = "good"
    last_name = "luck"
    email = "hello@trootech.com"

    def setUp(self):
        self.user = Customer.objects.create_user(
            username=self.username,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )

        return DELETE_USER_PAYLOAD.update(self.user.__dict__)

    def test_delete_user(self):
        """
        It should test delete API for user.
        """

        user_id = DELETE_USER_PAYLOAD.get("id")
        response = self.client.delete(BASE_URL + str(user_id) + "/")
        response_data_count = len(response.content)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(response_data_count, DELETE_COUNT)


class TestBusinessUserAPI:
    def setUp(self, register_business):
        self.business = {
            "business_customer": register_business.business_customer.id,
            "company_name": "trootech",
            "phone_number": "9999999999",
            "company_email": register_business.company_email,
            "revenue": register_business.revenue,
            "Year_of_Establishment": "23-03-2015",
            "product_category": "somethig",
            "company_profile": register_business.company_profile,
            "portfolio": register_business.portfolio,
            "offline_channel": register_business.offline_channel,
        }
        return BUSINESS_USER_PAYLOAD.update(self.business)

    def test_post_form_business(self, api_client, register_business):
        """It should test business post API."""
        before_business_count = Business.objects.all().count()
        api_client.force_authenticate(register_business.business_customer)
        self.setUp(register_business)
        response = api_client.post(
            BUSINESS_USER_URL, data=BUSINESS_USER_PAYLOAD, format="json"
        )
        after_business_count = Business.objects.all().count()
        assert response.status_code == HTTP_201_CREATED
        assert after_business_count == before_business_count + 1

    def test_delete_business(self, api_client, register_business):
        """It should test for removing registered business."""
        api_client.force_authenticate(register_business.business_customer)

        response = api_client.delete(
            BUSINESS_USER_URL + str(register_business.pk) + "/"
        )
        response_data_count = len(response.content)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert response_data_count == DELETE_COUNT

    def test_get_form_math_business_user_to_request_user(
            self, api_client, register_business
    ):
        """
        It should test that business user and request user is same.
        """
        api_client.force_authenticate(register_business.business_customer)
        response = api_client.get(
            BUSINESS_USER_URL, data=BUSINESS_USER_PAYLOAD, format="json"
        )
        user = response.json().get("results")
        assert response.status_code == HTTP_200_OK
        assert user[0]["business_customer"] == register_business.business_customer.id

    def test_staff_user(self, api_client, register_business):
        """
        Only registered business user can add staff members.
        """
        before_customer_data = Customer.objects.all().count()
        api_client.force_authenticate(register_business.business_customer)
        data = {
            "id": register_business.business_customer.id,
            "staff_members": [
                {
                    "username": "yogi",
                    "email": "yogi@gmail.com",
                    "first_name": "yo",
                    "last_name": "aadityanath",
                    "date_joined": "1992-04-21",
                    "birth_date": "18-03-1979",
                    "address": "UttarPradesh",
                    "gender": "male",
                    "phone_number": 1234567891,
                    "age": 45,
                    "password": "yogi1234##",
                    "password2": "yogi1234##",
                    "is_staff": 0,
                    "manager": register_business.business_customer.id,
                }
            ],
        }
        response = api_client.put(
            STAFF_REGISTRATION + str(register_business.business_customer.pk) + "/",
            data=data,
            format="json",
        )
        after_customer_data = Customer.objects.all().count()
        assert response.status_code == HTTP_200_OK
        assert after_customer_data == before_customer_data + 1


class TestStaffUser:
    def setUp(self, business_user):
        self.user_payload = {
            "id": business_user.business_customer.id,
            "staff_members": [
                {
                    "username": "yogi",
                    "email": "yogi@gmail.com",
                    "first_name": "yo",
                    "last_name": "aadityanath",
                    "date_joined": "1992-04-21",
                    "birth_date": "18-03-1979",
                    "address": "UttarPradesh",
                    "gender": "male",
                    "phone_number": 1234567891,
                    "age": 45,
                    "password": "yogi1234##",
                    "password2": "yogi1234##",
                    "is_staff": 0,
                    "manager": business_user.business_customer.id,
                }
            ],
        }
        return STAFF_USER_PAYLOAD.update(self.user_payload)

    def test_get_form_manager_to_request_user(self, api_client, register_business):
        """
        only that user add staff members who registered any company.
        """
        api_client.force_authenticate(register_business.business_customer)
        self.setUp(register_business)
        response = api_client.get(
            STAFF_REGISTRATION, data=STAFF_USER_PAYLOAD, format="json"
        )
        user = response.json().get("results")
        assert response.status_code == HTTP_200_OK
        assert user[0]["username"] == register_business.business_customer.username
