from django.test import TestCase

from .models import Lobby, UserProfile
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


class SessionMethodTests(TestCase):
    pass


class TerritoryMethodTests(TestCase):
    pass


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
