from django.test import TestCase

from .models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class LobbyMethodTests(TestCase):
    def setUp(self):
        """
        Create needed instances of models.
        """
        self.lobby_test = Lobby.objects.create(name="RandomName")

    def tearDown(self):
        """
        Delete created instances after a test.
        """
        self.lobby_test.delete()

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
    def setUp(self):
        """
        Create needed instances of models.
        """
        self.ter1 = Territory.objects.create(name="Territory_name", description="Some description")

    def tearDown(self):
        """
        Delete created instances after a test.
        """
        self.ter1.delete()

    def test_ensure_food_is_not_negative(self):
        """
        Ensures the food is always non-negative. Checks if the value is normalized
        when a negative one has been set.
        """
        self.ter1.food = -5
        self.ter1.save()
        self.assertGreaterEqual(self.ter1.food, 0, "Food cannot be negative!")

    def test_ensure_gold_is_not_negative(self):
        """
        Ensures the gold is always non-negative. Checks if the value is normalized
        when a negative one has been set.
        """
        self.ter1.gold = -5
        self.ter1.save()
        self.assertGreaterEqual(self.ter1.gold, 0, "Gold cannot be negative!")

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
    def setUp(self):
        """
        Create needed instances of models.
        """
        self.user_test = User.objects.create_user(username="user", email="user@user.user", password="Iamjustauser17")
        self.lobby_test = Lobby.objects.create(name="RandomName")
        self.session_test = Session.objects.create(user=self.user_test, lobby=self.lobby_test)
        self.territory_test = Territory.objects.create(name="Territory_name", description="Some description")
        self.territory_session_test = TerritorySession.objects.create(territory=self.territory_test,
                                                                      lobby=self.lobby_test,
                                                                      owner=self.session_test)

    def tearDown(self):
        """
        Delete created instances after a test.
        """
        self.user_test.delete()
        self.lobby_test.delete()
        self.session_test.delete()
        self.territory_test.delete()
        self.territory_session_test.delete()

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
    def setUp(self):
        """
        Create needed instances of models.
        """
        self.user1 = User.objects.create_user(username="user", email="user@user.user", password="Useruser17")
        self.user1_profile = UserProfile.objects.get_or_create(user=self.user1)[0]
        self.user2 = User.objects.create_user(username="user1", email="user1@user1.user", password="User1user117")
        self.user2profile = UserProfile.objects.get_or_create(user=self.user2)[0]

    def tearDown(self):
        """
        Delete created instances after a test.
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


class IndexAboutTermsViewsTests(TestCase):
    """
    This class tests the index, the about, and the Terms and conditions views.
    They are basic with not much information to be tested, hence, they are combined.
    """

    def test_ensure_about_loads(self):
        """
        Ensure the about page loads - status code 200.
        """
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_ensure_index_loads(self):
        """
        Ensure the index page loads - status code 200.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_ensure_terms_and_conditions_loads(self):
        """
        Ensure the terms and conditions page loads - status code 200.
        """
        response = self.client.get(reverse('termsandconditions'))
        self.assertEqual(response.status_code, 200)


class LeaderBoardViewTests(TestCase):
    def test_ensure_login_required(self):
        """
        Ensure anonymous users cannot access the leader board and get redirected to the login page.
        """
        response = self.client.get(reverse('leaderboard'))
        self.assertRedirects(response, reverse('auth_login') + "?next=/leaderboard/", status_code=302,
                             target_status_code=200)

    def test_ensure_user_is_logged_in(self):
        pass

    def test_ensure_leader_board_is_empty(self):
        pass

    def test_ensure_leader_board_is_not_empty(self):
        pass

    def test_ensure_users_are_sorted(self):
        pass


class CreateLobbyViewTests(TestCase):
    def test_ensure_login_required(self):
        """
        Ensure anonymous users cannot access the Create Lobby view and get redirected to the login page.
        """
        response = self.client.get(reverse('lobbycreate'))
        self.assertRedirects(response, reverse('auth_login') + "?next=/lobby/create/", status_code=302,
                             target_status_code=200)

    def test_ensure_user_is_logged_in(self):
        """
        Ensure registered users can access the Create Lobby view.
        """
        # create a user so we can access the page
        self.user_test = User.objects.create_user(username="user", email="user@user.user", password="Iamjustauser17")
        self.client.login(username="user", password="Iamjustauser17")
        response = self.client.get(reverse('lobbycreate'))
        self.assertEqual(response.status_code, 200)

    def test_ensure_logged_in_user_creates_lobby(self):
        """
        Ensure registered users can access the Create Lobby view and create a lobby.
        """
        # create a user so we can create a lobby
        self.user_test = User.objects.create_user(username="user", email="user@user.user", password="Iamjustauser17")
        self.client.login(username="user", password="Iamjustauser17")
        # make mock-up post request and create the lobby with the given name
        self.client.post(reverse('lobbycreate'), {"name": "FCBarcelona"})
        # make sure the lobby is created by getting it from the data base, if not it throws an exception
        Lobby.objects.get(name="FCBarcelona")
        # if code gets here, the lobby was created and an exception was not thrown
        self.assertTrue(True)
