from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase

from customer.factories import CustomerFactory

TOKEN_URL = 'http://127.0.0.1:8000/api/v1/get_token/'
REGISTER_URL = 'http://127.0.0.1:8000/api/v1/register/'


# class TestUserViewSet:
#     def test_register(self, api_factory, authenticate_user):
#         data = {
#             'username': authenticate_user.username,
#             'password': authenticate_user.password,
#             'first_name': authenticate_user.first_name,
#             'last_name': authenticate_user.last_name,
#             'email': authenticate_user.email,
#             'date_joined': '2018-01-18 12:02:01.003',
#             'birth_date': authenticate_user.birth_date,
#             'gender': authenticate_user.gender,
#             'phone_number': authenticate_user.phone_number
#
#         }
#         response = api_factory.post(
#             REGISTER_URL,
#             data=data, format='json'
#         )
#         # assert (response.status_code == HTTP_200_OK)
#         assert response.read()
#
#     def test_login(self, api_factory, authenticate_user):
#         data = {
#             'username': authenticate_user.username,
#             'password': authenticate_user.password
#         }
#         # api_factory.force_authenticate(authenticate_user)
#         response = api_factory.post(
#             TOKEN_URL,
#             data=data,
#             format='json',
#         )
#         # assert (response.status_code == HTTP_200_OK)
#         assert response.read()
#         token = Token.objects.get(user=authenticate_user)
#         assert (token.key == response.data['token'])
#
#     def test_token(self, api_factory, authenticate_user, api_client):
#         response = api_factory.post(TOKEN_URL,
#                                     {"username": authenticate_user.username, "password": authenticate_user.password})
#         # assert response.status_code == HTTP_200_OK
#         response_content = json.loads(response.content.decode('utf-8'))
#         token = response_content["token"]
#         response = api_factory.post("/auth/api/authenticated/", {}, Authorization='JWT ' + token)
#         response_content = json.loads(response.content.decode('utf-8'))
#
#         assert response_content["authenticated"]


class LoginTests(APITestCase):
    def setUp(self):
        self.user = CustomerFactory.create()
        self.jwt_url = TOKEN_URL

    def test_post_form_failing_jwt_auth(self):
        """
        Ensure POSTing form over JWT auth without correct credentials fails
        """
        data = {
            'username': self.user.username,
            'password': 'inCorrect01'
        }
        response = self.client.post(self.jwt_url, data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_token_login_success(self):
        """
        Ensures posting from over JWT auth with correct credentials only
        """
        self.client.force_authenticate(self.user)
        data = {
            'username': self.user.username,
            'password': self.user.password,
        }
        response = self.client.post(self.jwt_url, data)
        self.assertNotEqual(response.data.get("refresh_token"), None)


