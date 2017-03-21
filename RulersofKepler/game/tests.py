from django.test import TestCase

from .models import Lobby


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
