import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from hangerapi.models import Cuisine

class CuisineTest(APITestCase):
    fixtures = ['cuisines', 'users', 'tokens']

    def setUp(self):
        self.user = User.objects.first()
        tokens = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {tokens.key}")

    def test_get_all_cuisines(self):
        
        """Ensure we can get a list of cuisines
        """
        response = self.client.get(f"/cuisines")
       
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response[0]["type"], "Chinese")
        self.assertEqual(json_response[1]["type"], "Italian")
        self.assertEqual(json_response[2]["type"], "Thai")
        self.assertEqual(json_response[3]["type"], "Mexican")
        self.assertEqual(json_response[4]["type"], "Japanese")
        self.assertEqual(json_response[5]["type"], "BBQ")
        self.assertEqual(json_response[6]["type"], "Burgers")
        self.assertEqual(json_response[7]["type"], "Strictly Tots and Mules")

    def test_get_a_single_cuisine(self):
        """Ensure we can get an existing cuisine
        """
        cuisine = Cuisine()
        cuisine.type = "Chinese"
        cuisine.save()
        
        # Initiate request and store response
        response = self.client.get(f"/cuisines/1")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["type"], "Chinese")

