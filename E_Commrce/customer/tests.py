

class TestUserViewSet:
    endpoint = '/user/'

    def test_list(self, client):
        client.force_authenticate(user=client)
        response = client.get(self.endpoint)
        return response
