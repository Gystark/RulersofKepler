from django.test import TestCase, Client

from .models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

client = Client()
user_test = None


def create_custom_user():
    user_test = User.objects.create_user(username="user", email="user@user.user", password="Iamjustauser17")
    client.login(username="user", password="Iamjustauser17")


class LobbyMethodTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create needed instances of models.
        """
        cls.lobby_test = Lobby.objects.create(name="RandomName")

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


class TerritoryMethodTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create needed instances of models.
        """
        cls.ter1 = Territory.objects.create(name="Territory_name", description="Some description")

    def test_ensure_food_is_not_negative(self):
        """
        Ensures the food is always non-negative. Checks if the value is normalized
        when a negative one has been set.
        """
        self.ter1.default_food = -5
        self.ter1.save()
        self.assertGreaterEqual(self.ter1.default_food, 0, "Food cannot be negative!")

    def test_ensure_gold_is_not_negative(self):
        """
        Ensures the gold is always non-negative. Checks if the value is normalized
        when a negative one has been set.
        """
        self.ter1.default_gold = -5
        self.ter1.save()
        self.assertGreaterEqual(self.ter1.default_gold, 0, "Gold cannot be negative!")

    def test_ensure_population_is_not_negative(self):
        """
        Ensures the population is always non-negative. Checks if the value is normalized
        when a negative one has been set.
        """
        self.ter1.default_population = -5
        self.ter1.save()
        self.assertGreaterEqual(self.ter1.default_population, 0, "Population cannot be negative!")

    def test_ensure_army_is_not_negative(self):
        """
        Ensures the army is always non-negative. Checks if the value is normalized
        when a negative one has been set.
        """
        self.ter1.default_army = -5
        self.ter1.save()
        self.assertGreaterEqual(self.ter1.default_army, 0, "Army cannot be negative!")


class TerritorySessionMethodTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create needed instances of models.
        """
        cls.user_test = User.objects.create_user(username="user", email="user@user.user", password="Iamjustauser17")
        cls.lobby_test = Lobby.objects.create(name="RandomName")
        cls.session_test = Session.objects.create(user=cls.user_test, lobby=cls.lobby_test)
        cls.territory_test = Territory.objects.create(name="Territory_name", description="Some description")
        cls.territory_session_test = TerritorySession.objects.create(territory=cls.territory_test,
                                                                     lobby=cls.lobby_test,
                                                                     owner=cls.session_test)

    def test_ensure_population_is_not_negative(self):
        """
        Ensures the population is always non-negative. Checks if the value is normalized
        when a negative one has been set.
        """
        self.territory_session_test.population = -5
        self.territory_session_test.save()
        self.assertGreaterEqual(self.territory_session_test.population, 0,
                                "TerritorySession population cannot be negative!")

    def test_ensure_army_is_not_negative(self):
        """
        Ensures the army is always non-negative. Checks if the value is normalized
        when a negative one has been set.
        """
        self.territory_session_test.army = -5
        self.territory_session_test.save()
        self.assertGreaterEqual(self.territory_session_test.army, 0, "TerrytorySession army cannot be negative!")

    def test_change_territory_owner_user_in_lobby(self):
        """
        Ensures the territory session's owner can be a user that is in the associated game. Another user
        in the same game is created. Returns True if the ownership can be changed.
        """
        # create another user and associated session - the lobby is the same
        self.another_user = User.objects.create_user(username="another_user", email="another@ano.ano",
                                                     password="IamsecondUser18")
        self.another_session = Session.objects.create(user=self.another_user, lobby=self.lobby_test)

        self.territory_session_test.change_owner(self.another_session)
        self.assertEquals(self.territory_session_test.owner, self.another_session)

    def test_change_territory_owner_user_not_in_lobby_throws_exception(self):
        """
        Ensures the territory session's owner can be a user that is in the associated game. Another user
        from another game/session is created. Throws ObjectDoesNotExist exception if the ownership
        cannot be changed i.e. the "new" owner is not part of the same game.
        """
        from django.core.exceptions import ObjectDoesNotExist

        # create third user that is not in the same lobby
        self.outsider_user = User.objects.create_user(username="outsider", email="outsider@out.out",
                                                      password="IamthirdUser19")
        # create a different lobby
        self.outsider_another_lobby = Lobby.objects.create(name="AnotherLobby")
        self.outsider_another_session = Session.objects.create(user=self.outsider_user,
                                                               lobby=self.outsider_another_lobby)
        # raise if there is no such user in this game
        self.assertRaises(ObjectDoesNotExist, self.territory_session_test.change_owner, self.outsider_another_session)


class UserProfileMethodTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create needed instances of models.
        """
        cls.user1 = User.objects.create_user(username="user", email="user@user.user", password="Useruser17")
        cls.user1_profile = UserProfile.objects.get_or_create(user=cls.user1)[0]
        cls.user2 = User.objects.create_user(username="user1", email="user1@user1.user", password="User1user117")
        cls.user2profile = UserProfile.objects.get_or_create(user=cls.user2)[0]

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


class SessionMethodTests(TestCase):
    """
    Test for the custom methods in the Session model.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test", email="test@test.test", password="test")
        cls.session = Session.objects.create(user=cls.user)

    def test_ensure_colour_is_not_none(self):
        """
        Test that the session gets a random colour assigned on saving and that
        it doesn't stay None.
        """
        self.assertNotEqual(self.session.colour, None)

    def test_ensure_colour_is_not_empty_string(self):
        """
        Test that the session gets a random colour assigned on saving and that
        it doesn't stay an empty string.
        """
        self.assertNotEqual(self.session.colour, '')


class IndexAboutTermsGameOverGameWonViewsTests(TestCase):
    """
    This class tests the index, the about, and the Terms and conditions views.
    They are basic with not much information to be tested, hence, they are combined.
    """

    def test_ensure_game_over_loads(self):
        """
        Ensure the about page loads - status code 200.
        """
        response = client.get(reverse('game-over'))
        self.assertEqual(response.status_code, 200)

    def test_ensure_game_won_loads(self):
        """
        Ensure the about page loads - status code 200.
        """
        response = client.get(reverse('game-won'))
        self.assertEqual(response.status_code, 200)

    def test_ensure_about_loads(self):
        """
        Ensure the about page loads - status code 200.
        """
        response = client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_ensure_index_loads(self):
        """
        Ensure the index page loads - status code 200.
        """
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_ensure_terms_and_conditions_loads(self):
        """
        Ensure the terms and conditions page loads - status code 200.
        """
        response = client.get(reverse('termsandconditions'))
        self.assertEqual(response.status_code, 200)


class LeaderBoardViewTests(TestCase):
    def test_ensure_login_required(self):
        """
        Ensure anonymous users cannot access the leader board and get redirected to the login page.
        """
        response = client.get(reverse('leaderboard'))
        self.assertRedirects(response, reverse('auth_login') + "?next=/leaderboard/", status_code=302,
                             target_status_code=200)

    def test_ensure_user_is_logged_in(self):
        """
        Ensure authenticated users can access the leader board.
        """
        # create a user so we can access the page
        create_custom_user()

        response = client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)

    def test_ensure_leader_board_has_initially_only_one_user(self):
        """
        Ensure the leader board initially consists of just 1 user - the newly registered one.
        """
        # create a user so we can access the page
        user_test1 = User.objects.create_user(username="user", email="user@user.user", password="Iamjustauser17")
        client.login(username="user", password="Iamjustauser17")

        response = client.get(reverse('leaderboard'))

        # count the number of users
        leader_board_users_size = User.objects.all().count()

        # ensure the number of initial users is just 1
        self.assertEqual(leader_board_users_size, 1, "Leader board should have only 1 user!")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user_test1.username)


class CreateLobbyViewTests(TestCase):
    def test_ensure_login_required(self):
        """
        Ensure anonymous users cannot access the Create Lobby view and get redirected to the login page.
        """
        response = client.get(reverse('lobbycreate'))
        self.assertRedirects(response, reverse('auth_login') + "?next=/lobby/create/", status_code=302,
                             target_status_code=200)

    def test_ensure_user_is_logged_in(self):
        """
        Ensure registered users can access the Create Lobby view.
        """
        # create a user so we can access the page
        create_custom_user()

        response = client.get(reverse('lobbycreate'))
        self.assertEqual(response.status_code, 200)

    def test_ensure_logged_in_user_creates_lobby(self):
        """
        Ensure registered users can access the Create Lobby view and create a lobby.
        """
        # create a user so we can create a lobby
        create_custom_user()

        # make mock-up post request and create the lobby with the given name
        client.post(reverse('lobbycreate'), {"name": "FCBarcelona"})

        # make sure the lobby is created by getting it from the data base, if not it throws an exception
        Lobby.objects.get(name="FCBarcelona")

        # if code gets here, the lobby was created and an exception was not thrown
        self.assertTrue(True)


class LobbyListViewTests(TestCase):
    def test_ensure_login_required(self):
        """
        Ensure anonymous users cannot access the Lobby list view and get redirected to the login page.
        """
        response = client.get(reverse('lobbylist'))
        self.assertRedirects(response, reverse('auth_login') + "?next=/lobby/list/", status_code=302,
                             target_status_code=200)

    def test_ensure_user_is_logged_in(self):
        """
        Ensure registered users can access the Lobby list view.
        """
        # create a user so we can access the page
        create_custom_user()

        response = client.get(reverse('lobbylist'))
        self.assertEqual(response.status_code, 200)

    def test_lobby_is_empty(self):
        """
        Ensure the lobby list is initially empty.
        """
        # create a user so we can access the page
        create_custom_user()

        response = client.get(reverse('lobbylist'))

        # count the number of lobbies
        lobbies_count = Lobby.objects.all().count()

        # ensure the number is 0 and the user is notified
        self.assertEqual(lobbies_count, 0, "Lobby list should be empty!")
        self.assertContains(response, "No lobbies available.")

    def test_lobby_is_not_empty(self):
        """
        A registered user creates a lobby. Ensure the lobby is saved in the data base and shown on the page.
        """
        # authenticate user so we can access the list lobby page
        create_custom_user()

        # create lobby so we test if it's shown and get the number of lobbies in the game
        Lobby.objects.create(name="LobbyTest")

        response = client.get(reverse('lobbylist'))

        # assert the number of lobbies in the data base is 1
        lobbies_count = Lobby.objects.all().count()

        self.assertEqual(lobbies_count, 1, "Lobby list should have length 1!")
        self.assertEqual(response.status_code, 200, "Status code not 200!")
        self.assertContains(response, "LobbyTest")

    def test_ensure_user_redirected_to_game(self):
        """
        Ensure the user is redirected to previously joined game.
        """
        # authenticate user so we can access the list lobby page
        user_test1 = User.objects.create_user(username="user", email="user@user.user", password="Iamjustauser17")
        client.login(username="user", password="Iamjustauser17")

        # create a lobby and a session that will be associated with the user
        lobby_test = Lobby.objects.create(name="LobbyTest")
        Session.objects.create(active=True, user=user_test1, lobby=lobby_test)

        # make sure the user is redirected to a game they previously joined.
        response = client.get(reverse('lobbylist'))
        self.assertRedirects(response, reverse('game', kwargs={"lobby_id": lobby_test.id}), status_code=302,
                             target_status_code=200)


class LobbyJoinViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create lobby which the user tries to join in.
        """
        cls.lobby_test = Lobby.objects.create(name="LobbyTest")
        cls.lobby_test_id = cls.lobby_test.id

    def test_ensure_login_required(self):
        """
        Ensure anonymous users cannot access the Lobby join view and get redirected to the login page.
        """
        response = client.get(reverse('lobbyjoin', kwargs={"lobby_id": self.lobby_test_id}))
        self.assertRedirects(response, reverse('auth_login') + "?next=/lobby/" + str(self.lobby_test_id) + "/join/",
                             status_code=302,
                             target_status_code=200)

    def test_ensure_user_logged_in_and_redirected_to_game(self):
        """
        Ensure registered users can access the Lobby join view and get redirected to previously joined game.
        """
        # create a user so we can access the page
        user_test1 = User.objects.create_user(username="user", email="user@user.user", password="Iamjustauser17")
        client.login(username="user", password="Iamjustauser17")

        # ensure the user already has a session in a game
        Session.objects.create(user=user_test1, lobby=self.lobby_test, active=True)

        # redirect the user to previously joined/created game
        response = client.get(reverse('lobbyjoin', kwargs={"lobby_id": self.lobby_test_id}))
        self.assertRedirects(response, reverse('game', kwargs={"lobby_id": self.lobby_test_id}), status_code=302,
                             target_status_code=200)

    def test_ensure_session_not_found_throws_exception(self):
        """
        Ensure if the user does not have a session, an exception is thrown and the view proceeds to execute
        the code in the "except" block.
        """
        # create a user so we can access the page
        create_custom_user()

        # try redirect the user to previously joined/created game
        # but user does not have one(Session), so throw exception and then do whatever
        try:
            response = client.get(reverse('lobbyjoin', kwargs={"lobby_id": self.lobby_test_id}))
        except ObjectDoesNotExist:
            self.assertTrue(True)
        else:
            self.assertFalse(True, "Session already existed, user was redirected to their game!")


class GameViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create lobby which the user tries to join in.
        """
        cls.lobby_test = Lobby.objects.create(name="LobbyTest")
        cls.lobby_test_id = cls.lobby_test.id

    def test_ensure_login_required(self):
        """
        Ensure anonymous users cannot access the game view and get redirected to the login page.
        """
        response = client.get(reverse('game', kwargs={"lobby_id": self.lobby_test_id}))
        self.assertRedirects(response, reverse('auth_login') + "?next=/game/" + str(self.lobby_test_id) + "/",
                             status_code=302,
                             target_status_code=200)

    def test_ensure_logged_in_user_is_redirected(self):
        """
        Ensure an authenticated user is redirected to the game view.
        """
        # create a user so we can access the page
        user_test1 = User.objects.create_user(username="user", email="user@user.user", password="Iamjustauser17")
        client.login(username="user", password="Iamjustauser17")

        # create a session the user is associated with
        Session.objects.create(lobby=self.lobby_test, user=user_test1, active=True)

        # ensure the game page loads for an authenticated user with a session
        response = client.get(reverse('game', kwargs={"lobby_id": self.lobby_test_id}))
        self.assertEqual(response.status_code, 200)

    def test_ensure_sessionless_user_redirected_to_lobbylist(self):
        """
        Ensure a user without a session is redirected to the lobby list page.
        """
        # create a user so we can access the page
        create_custom_user()

        # a user without a session is redirected to the lobby list
        response = client.get(reverse('game', kwargs={"lobby_id": self.lobby_test_id}))
        self.assertRedirects(response, reverse('lobbylist'), status_code=302, target_status_code=200)


class ProfileViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Create a user for viewing.
        """
        cls.another_user_test = User.objects.create_user(username="user2", email="user2@user2.user2",
                                                         password="Iamjustanotheruser18")

    def test_ensure_login_required(self):
        """
        Ensure anonymous users cannot view registered users' profiles.
        """
        # anonymous user should be redirected to the login page
        response = client.get(reverse('profile', kwargs={"username": self.another_user_test.username}))
        self.assertRedirects(response,
                             reverse('auth_login') + "?next=/profile/" + str(self.another_user_test.username) + "/",
                             status_code=302,
                             target_status_code=200)

    def test_ensure_user_is_logged_in(self):
        """
        Ensure registered users can view other users' profiles.
        """
        # create a user so we can access the page
        create_custom_user()

        # ensure the page loads with success code
        response = client.get(reverse('profile', kwargs={"username": self.another_user_test.username}))
        self.assertEqual(response.status_code, 200)

    def test_ensure_exception_is_thrown_when_no_such_user_exists(self):
        """
        Ensure the user is redirected to the index page when they try to view the profile of a non-existing user.
        """
        # create a user so we can access the page
        create_custom_user()

        unknown_user_username = "anonymous"

        response = client.get(reverse('profile', kwargs={"username": unknown_user_username}))
        self.assertRedirects(response, reverse('index'))
