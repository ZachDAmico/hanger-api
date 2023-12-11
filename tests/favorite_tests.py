import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from hangerapi.models import Favorite



class FavoriteTest(APITestCase):
    fixtures = ['users', 'tokens', 'restaurants']

    def setUp(self):
        self.user = User.objects.first()
        tokens = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {tokens.key}")

    def test_create_favorite(self):
        """
        Ensure we can create a new favorite
        """
        url = "/favorites"

        data = {
            "user": 1,
            "restaurant": 5
        }
        response = self.client.post(url, data, format='json')

        print(response.content)
        print(response.data)
        print(response.status_code)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["user_id"], 1)
        self.assertEqual(json_response["restaurant_id"], 5)