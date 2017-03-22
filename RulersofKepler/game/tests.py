from django.test import TestCase

from .models import Lobby, UserProfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class ModelTests(TestCase):
    def test_default_lobby_name_none(self):
        """
        The name of the lobby should be set to Lobby 1 when given a None as its name.
        """
        lobby = Lobby.objects.create(name=None)
        self.assertEqual(lobby.name, "Lobby 1")

    def test_default_lobby_name_empty_string(self):
        """
        The name of the lobby should be set to Lobby 1 when given an empty string as its name.
        """
        lobby = Lobby.objects.create(name="")
        self.assertEqual(lobby.name, "Lobby 1")

    def test_default_lobby_name_preserved(self):
        """
        The name of the lobby should be preserved when it is not None or empty string.
        """
        lobby = Lobby.objects.create(name="test_lobby")
        self.assertEqual(lobby.name, "test_lobby")


class UserProfileMethodTests(TestCase):
    def test_ensure_games_played_are_not_negative(self):
        """
        ensure_games_played_are_not_negative should result True for user profiles
        where games_played are zero or positive
        """
        my_user = User.objects.create_user(username="user", email="user@user.user", password="Useruser17")
        my_user_profile = UserProfile.objects.get_or_create(user=my_user)[0]
        my_user_profile.games_played = -1
        my_user_profile.games_won = 0
        my_user_profile.save()
        my_user.save()
        self.assertEqual(my_user_profile.games_played >= 0, True)

    def test_ensure_games_won_are_not_negative(self):
        """
        ensure_games_won_are_not_negative should result True for user profiles
        where games_won are zero or positive
        """
        my_user = User.objects.create_user(username="user", email="user@user.user", password="Useruser17")
        my_user_profile = UserProfile.objects.get_or_create(user=my_user)[0]
        my_user_profile.games_played = 0
        my_user_profile.games_won = -5
        my_user_profile.save()
        my_user.save()
        self.assertEqual(my_user_profile.games_won >= 0, True)


class AboutViewTests(TestCase):
    def test_ensure_about_loads(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is the 'about' page")
        self.assertEqual(response.context["name"], "kepler")

