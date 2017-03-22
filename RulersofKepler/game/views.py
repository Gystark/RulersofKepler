from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from random import uniform, randrange

from .models import *
from .forms import LobbyCreationForm

# The maximum number of sessions that can join a lobby
MAX_SESSIONS = 4


def index(request):
    return render(request, "game/index.html", {})


@login_required
def lobbylist(request):
    """
    List all lobbies which have less than the maximum number of players.
    """
    try:
        sess = Session.objects.get(active=True, user=request.user)
        return redirect('game', lobby_id=sess.lobby.id)
    except Session.DoesNotExist:
        lobbies = Lobby.objects.all().exclude(session=MAX_SESSIONS)

        # Add player count to each lobby
        for lobby in lobbies:
            lobby.players = Session.objects.filter(lobby=lobby).count()

        return render(request, "game/lobbylist.html", {'lobbies': lobbies, "max_sessions": MAX_SESSIONS})


def get_initial_territory(lobby):
    """
    Get a random territory that doesn't have an owner
    """
    while True:
        terr_id = randrange(1, 19)
        ts = TerritorySession.objects.get(lobby=lobby, territory__id=terr_id)
        if not ts.owner:
            return ts


@login_required
def lobbyjoin(request, lobby_id):
    """
    Join the lobby specified by lobby_id
    """
    try:
        sess = Session.objects.get(active=True, user=request.user)
        return redirect('game', lobby_id=sess.lobby.id)
    except Session.DoesNotExist:
        try:
            lobby = Lobby.objects.get(id=lobby_id)
            Session.objects.create(user=request.user, lobby=lobby, active=True)
            sess = Session.objects.get(user=request.user, lobby=lobby, active=True)
            initial_terr = get_initial_territory(lobby)
            initial_terr.owner = sess
            initial_terr.save()
            return redirect('game', lobby_id=lobby.id)
        except Lobby.DoesNotExist:
            messages.error(request, 'Error joining the lobby, please try again.')
            return redirect('lobbylist')


@login_required
def lobbycreate(request):
    """
    Create a new lobby.
    """
    if request.method == "POST":
        form = LobbyCreationForm(request.POST)

        if form.is_valid():
            lobby = Lobby.objects.create(name=form.cleaned_data.get("name"))
            return redirect('lobbyjoin', lobby_id=lobby.id)
        else:
            messages.error(request, "Failed to create the lobby, please try again.")
        return render(request, "game/lobbycreate.html", {"form": form})
    else:
        form = LobbyCreationForm
    return render(request, "game/lobbycreate.html", {"form": form})


def about(request):
    """
    Render the static about us page.
    """
    context_dict = {"name": "kepler"}
    return render(request, "game/about.html", context=context_dict)


@login_required
def game(request, lobby_id):
    try:
        Session.objects.get(user=request.user, active=True)
        return render(request, "game/game.html", {'lobby': lobby_id})
    except Session.DoesNotExist:
        return redirect('lobbylist')


@login_required
def leaderboard(request):
    """
    Compute and return the top 10 players.
    """
    # TODO replace the dummy values when we've decided on scoring
    stats = []
    users = User.objects.all()
    for user in users:
        magic_value = Session.objects.filter(user=user).count()

        stats.append({"name": user.username, "wins": magic_value, "losses": magic_value, "ratio": magic_value})
    return render(request, "game/leaderboard.html", {"stats": stats})


@login_required
def profile(request, username):
    # get the user object or redirect to index page
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    # get additional information about the user
    userprofile = UserProfile.objects.get_or_create(user=user)[0]

    # calculate lost games
    games_lost = get_user_games_lost(userprofile)
    # calculate winning percentage
    win_percentage = get_user_win_percentage(userprofile)

    context_dict = {'selecteduser': user, "userprofile": userprofile, "games_lost": games_lost,
                    "win_percent": win_percentage}
    return render(request, "game/profile.html", context_dict)


def termsandconditions(request):
    return render(request, "game/terms.html", {})


def get_user_games_lost(userprofile):
    return userprofile.games_played - userprofile.games_won


def get_user_win_percentage(userprofile):
    try:
        return userprofile.games_won * 1.0 / userprofile.games_played
    except ZeroDivisionError:
        return 0


@login_required
def get_territory_all(request, lobby_id):
    """
    Return data for the given territory in the given lobby.
    """
    if request.is_ajax() and request.method == 'GET':
        try:
            territories = Territory.objects.all()
            response = {}
            for territory in territories:
                territory_session = TerritorySession.objects.get(territory=territory, lobby__id=lobby_id)
                owner = territory_session.owner.user.username if territory_session.owner is not None else ''
                colour = 'rgb' + territory_session.owner.colour if territory_session.owner is not None else 'rgb(0, 0, 0)'
                response.update({
                    territory.name:
                        {
                            'id': territory.id,
                            'name': territory.name,
                            'description': territory.description,
                            'population': territory_session.population,
                            'army': territory_session.army,
                            'food': territory.food,
                            'gold': territory.gold,
                            'coordinates': territory.coordinates,
                            'owner': owner,
                            'neighbours': territory_session.get_borders(),
                            'colour': colour,
                        }
                })
        except ObjectDoesNotExist:
            response = {'response': 'error'}

        return JsonResponse(response)

    # If the request is not ajax and POST, show an error
    messages.error(request, 'System error, please try again.')
    return redirect('index')


@login_required
def get_territory_reduced(request, lobby_id):
    """
    Return data for the given territory in the given lobby.
    """
    if request.is_ajax() and request.method == 'GET':
        try:
            Session.objects.get(lobby__id=lobby_id, user=request.user, active=True)

            territories = Territory.objects.all()
            response = {}
            for territory in territories:
                territory_session = TerritorySession.objects.get(territory=territory, lobby__id=lobby_id)
                owner = territory_session.owner.username if territory_session.owner is not None else ''
                colour = 'rgb' + territory_session.owner.colour if territory_session.owner is not None else 'rgb(0, 0, 0)'
                response.update({
                    territory.name:
                        {
                            'id': territory.id,
                            'name': territory.name,
                            'population': territory_session.population,
                            'army': territory_session.army,
                            'food': territory.food,
                            'gold': territory.gold,
                            'owner': owner,
                            'colour': colour,
                        }
                })
        except ObjectDoesNotExist:
            response = {'response': 'error'}

        return JsonResponse(response)

    # If the request is not ajax and POST, show an error
    messages.error(request, 'System error, please try again.')
    return redirect('index')


@login_required
def set_population_army(request):
    """
    Set the population of the given territory in the given lobby.
    """
    if request.is_ajax() and request.method == "POST" and 'territory_id' in request.POST and 'lobby_id' in request.POST and 'new_population' in request.POST and 'new_army' in request.POST:
        territory_id = request.POST.get('territory_id')
        lobby_id = request.POST.get('lobby_id')

        if territory_id is None or lobby_id is None:
            response = 'error'
        else:
            try:
                territory_session = TerritorySession.objects.get(territory__id=territory_id, lobby__id=lobby_id)

                new_population = request.POST.get('new_population')
                new_army = request.POST.get('new_army')
                new_total = new_population + new_army
                old_total = territory_session.population + territory_session.army

                if new_total == old_total and territory_session.owner == request.user:
                    territory_session.population = new_population
                    territory_session.army = new_army
                    territory_session.save()
                    response = "success"
                else:
                    response = "error"
            except ObjectDoesNotExist:
                response = 'error'

        return JsonResponse({'response': response})

    # If the request is not ajax and POST, show an error
    messages.error(request, 'System error, please try again.')
    return redirect('index')


@login_required
def move_army(request):
    """
    Move the specified amount of army from territory 1 to territory 2..
    """
    if request.is_ajax() and request.method == 'POST':
        lobby_id = request.POST.get('lobby_id')
        t1_id = request.POST.get('t1_id')
        t2_id = request.POST.get('t2_id')
        amount = request.POST.get('amount')

        if any((lobby_id, t1_id, t2_id, amount) is None):
            response = 'error'
        else:
            try:
                session_1 = TerritorySession.objects.get(lobby__id=lobby_id, territory__id=t1_id)
                session_2 = TerritorySession.objects.get(lobby__id=lobby_id, territory__id=t2_id)

                if session_1.territory.name in session_2.get_borders():

                    if session_1.army >= amount and session_1.owner == request.user and session_2.owner == request.user:
                        session_2.army += amount
                        session_1.army -= amount
                        session_1.save()
                        session_2.save()
                        response = 'success'
                    else:
                        response = 'error'

                else:
                    response = 'error'

            except ObjectDoesNotExist:
                response = 'error'

        return JsonResponse({'response': response})

    # If the request is not ajax and POST, show an error
    messages.error(request, 'System error, please try again.')
    return redirect('index')


def get_battle_winner(defend_terr, attack_terr):
    """
    Get the winner in a battle between two territories
    Also change the territory owner accordingly
    """
    # TODO decide on battle algorithm
    def_score = (defend_terr.army * 1.0 + 0.1 * defend_terr.population) * uniform(0.8, 1.2)
    att_score = (attack_terr.army * 1.0 + 0.1 * attack_terr.population) * uniform(0.8, 1.2)
    if att_score > def_score:
        defend_terr.change_owner(attack_terr.owner)
        defend_terr.army /= 2
        defend_terr.save()
        return attack_terr.owner.user
    attack_terr.army /= 2
    attack_terr.save()
    if defend_terr.owner != '' and defend_terr.owner is not None:
        return defend_terr.owner.user
    else:
        return ''


@login_required
def attack(request):
    """
    Attack territory 1 with the army in territory 2.
    """
    if request.is_ajax() and request.method == 'POST':
        lobby_id = request.POST.get('lobby_id')
        t1_id = request.POST.get('t1_id')
        t2_id = request.POST.get('t2_id')

        if any((lobby_id, t1_id, t2_id) is None):
            response = 'error'
        else:
            try:
                session_1 = TerritorySession.objects.get(lobby__id=lobby_id, territory__id=t1_id)
                session_2 = TerritorySession.objects.get(lobby__id=lobby_id, territory__id=t2_id)

                if session_1.name in session_2.get_borders():

                    attacker = session_2.owner.user
                    defender = session_1.owner.user

                    if attacker == request.user and defender != request.user:

                        winner = get_battle_winner(session_1, session_2)

                        if winner == request.user:
                            response = 'won'

                        else:
                            response = 'lost'
                    else:
                        response = 'error'

                else:
                    response = 'error'

            except ObjectDoesNotExist:
                response = 'error'

        return JsonResponse({'response': response})

    # If the request is not ajax and POST, show an error
    messages.error(request, 'System error, please try again.')
    return redirect('index')
