from django.test import TestCase

from .models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class LobbyMethodTests(TestCase):
    def setUp(self):
        self.lobby_test = Lobby.objects.create(name="RandomName")

    def test_default_lobby_name_none(self):
        """
        The name of the lobby should be set to "Lobby + lobby's id" when given a None as its name.
        """
        self.lobby_test.name = None
        self.lobby_test.save()
        self.assertEqual(self.lobby_test.name, "Lobby " + str(self.lobby_test.id))

    def test_default_lobby_name_empty_string(self):
        """
        The name of the lobby should be set to "Lobby + lobby's id" when given an empty string as its name.
        """
        self.lobby_test.name = ""
        self.lobby_test.save()
        self.assertEqual(self.lobby_test.name, "Lobby " + str(self.lobby_test.id))

    def test_default_lobby_name_preserved(self):
        """
        The name of the lobby should be preserved when it is not None or empty string.
        """
        self.lobby_test.name = "test_name"
        self.lobby_test.save()
        self.assertEqual(self.lobby_test.name, "test_name")

    def test_if_territories_are_generated_from_generate_function(self):
        """
        When a Lobby is created/saved, the number of territories associated with it should equal to
        the total number of Territory objects in the database.
        """
        # get all territories associated with a lobby
        generated_territories_size = TerritorySession.objects.filter(lobby=self.lobby_test).count()
        # and compare them to the total number of those in the db
        all_territories_size = Territory.objects.all().count()
        self.assertEqual(generated_territories_size, all_territories_size)


"""
    # TODO
        # test the active field when user enters a game and after they finish one

class SessionMethodTests(TestCase):
    def setUp(self):
        self.user_test = User.objects.create_user(username="user", email="user@user.user", password="Useruser17")
        self.lobby_test = Lobby.objects.create(name="RandomName")
        self.session_test = Session.objects.create(user=self.user_test, lobby=self.lobby_test)

    def tearDown(self):
        self.user_test.delete()
        self.lobby_test.delete()
        self.session_test.delete()
"""


class TerritoryMethodTests(TestCase):
    def setUp(self):
        self.ter1 = Territory.objects.create(name="Territory_name", description="Some description")

    def tearDown(self):
        self.ter1.delete()

    def test_ensure_food_is_not_negative(self):
        self.ter1.food = -5
        self.ter1.save()
        self.assertGreaterEqual(self.ter1.food, 0, "Food cannot be negative!")

    def test_ensure_gold_is_not_negative(self):
        self.ter1.gold = -5
        self.ter1.save()
        self.assertGreaterEqual(self.ter1.gold, 0, "Gold cannot be negative!")

    def test_ensure_population_is_not_negative(self):
        self.ter1.default_population = -5
        self.ter1.save()
        self.assertGreaterEqual(self.ter1.default_population, 0, "Population cannot be negative!")

    def test_ensure_army_is_not_negative(self):
        self.ter1.default_army = -5
        self.ter1.save()
        self.assertGreaterEqual(self.ter1.default_army, 0, "Army cannot be negative!")


class TerritorySessionMethodTests(TestCase):
    def setUp(self):
        self.user_test = User.objects.create_user(username="user", email="user@user.user", password="Useruser17")
        self.lobby_test = Lobby.objects.create(name="RandomName")
        self.session_test = Session.objects.create(user=self.user_test, lobby=self.lobby_test)
        self.territory_test = Territory.objects.create(name="Territory_name", description="Some description")
        self.territory_session_test = TerritorySession.objects.create(territory=self.territory_test,
                                                                      lobby=self.lobby_test,
                                                                      owner=self.session_test)

    def tearDown(self):
        self.user_test.delete()
        self.lobby_test.delete()
        self.session_test.delete()
        self.territory_test.delete()
        self.territory_session_test.delete()

    def test_ensure_population_is_not_negative(self):
        self.territory_session_test.population = -5
        self.territory_session_test.save()
        self.assertGreaterEqual(self.territory_session_test.population, 0,
                                "TerritorySession population cannot be negative!")

    def test_ensure_army_is_not_negative(self):
        self.territory_session_test.army = -5
        self.territory_session_test.save()
        self.assertGreaterEqual(self.territory_session_test.army, 0, "TerrytorySession army cannot be negative!")

    # TODO
        # test change owner function


class UserProfileMethodTests(TestCase):
    def setUp(self):
        """
        set up some users and their profiles
        """
        self.user1 = User.objects.create_user(username="user", email="user@user.user", password="Useruser17")
        self.user1_profile = UserProfile.objects.get_or_create(user=self.user1)[0]
        self.user2 = User.objects.create_user(username="user1", email="user1@user1.user", password="User1user117")
        self.user2profile = UserProfile.objects.get_or_create(user=self.user2)[0]

    def tearDown(self):
        """
        delete previously created users
        """
        self.user1.delete()
        self.user2.delete()

    def test_ensure_games_played_are_not_negative(self):
        """
        ensure_games_played_are_not_negative should result True for user profiles
        where games_played are zero or positive
        """
        self.user1_profile.games_played = -1
        self.user1_profile.games_won = 0
        self.user1_profile.save()
        self.assertEqual(self.user1_profile.games_played >= 0, True)

    def test_ensure_games_won_are_not_negative(self):
        """
        ensure_games_won_are_not_negative should result True for user profiles
        where games_won are zero or positive
        """
        self.user1_profile.games_played = 0
        self.user1_profile.games_won = -5
        self.user1_profile.save()
        self.assertEqual(self.user1_profile.games_won >= 0, True)


class AboutViewTests(TestCase):
    def test_ensure_about_loads(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the 'about' page")
        self.assertEqual(response.context["name"], "kepler")
