import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Event,Games,Gamer,GameType


class EventTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types

        gametype = GameType()
        gametype.label = "Board game"
        gametype.save()

        game = Games()
        game.gametype_id = 1
        game.skill_level = 5
        game.title = "Monopoly"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()


    def test_create_event(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/events"
        data = {
            "gameId": 1,
            "description": "Clue",
            "time": "19:45",
            "date":"2021-08-19"
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["game"]["id"], 1)
        self.assertEqual(json_response["description"], "Clue")
        self.assertEqual(json_response["time"], "19:45")
        self.assertEqual(json_response["date"], "2021-08-19")
        self.assertEqual(json_response["organizer"]["id"], 1)

    def test_get_event(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        event = Event()
        event.game_id = 1
        event.organizer_id=1
        event.time = "11:45:00"
        event.date = "2021-05-19"
        event.description= "budding software developer"

        event.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        # self.assertEqual(json_response["organizer"]["id"], "Monopoly")
        self.assertEqual(json_response["description"], "budding software developer")
        # self.assertEqual(json_response["game"]["id"], 5)
        self.assertEqual(json_response["time"], "11:45:00")
        self.assertEqual(json_response["date"], "2021-05-19")


    
    def test_change_event(self):
        """
        Ensure we can change an existing game.
        """
        event = Event()
        event.game_id = 1
        event.organizer_id=1
        event.time = "12:25:00"
        event.date = "2000-03-29"
        event.description= "junior software developer"

        event.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gameId": 1,
            "description": "Hasbro",
            "time": "12:25:00",
            "date":"2000-03-29"
            }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET EVENT AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        # self.assertEqual(json_response["gameId"], 1)
        self.assertEqual(json_response["description"], "Hasbro")
        self.assertEqual(json_response["time"],"12:25:00")
        self.assertEqual(json_response["date"], "2000-03-29")


    def test_delete_event(self):
        """
        Ensure we can delete an existing game.
        """
        event = Event()
        event.game_id = 1
        event.organizer_id=1
        event.time = "11:25:00"
        event.date = "2000-03-17"
        event.description= "senior software developer"

        event.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET event AGAIN TO VERIFY 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
