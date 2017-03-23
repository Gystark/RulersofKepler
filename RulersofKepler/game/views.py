from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect

from utils import get_initial_territory, get_user_games_lost, get_user_win_percentage, get_endgame, get_battle_winner
from .forms import LobbyCreationForm
from .models import Session, Lobby, Territory, TerritorySession, UserProfile

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
    return render(request, "game/about.html", {})


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
    stats = []
    users = User.objects.all()
    for user in users:
        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        # calculate lost games
        losses = get_user_games_lost(user_profile)
        # calculate winning percentage
        ratio = get_user_win_percentage(user_profile)

        stats.append({"name": user.username, "wins": user_profile.games_won, "losses": losses, "ratio": ratio})
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


def gamewon(request):
    return render(request, "game/gamewon.html", {})


def gameover(request):
    return render(request, "game/gameover.html", {})


@login_required
def get_territory_all(request, lobby_id):
    """
    Return data for the given territory in the given lobby.
    """
    if request.is_ajax() and request.method == 'GET':
        try:
            sess = Session.objects.get(lobby__id=lobby_id, user=request.user, active=True)

            result = get_endgame(sess)
            territories = Territory.objects.all()
            if result == "winner" or result == "loser":
                response = {'response': result}
            else:
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
                            'food': territory_session.food,
                            'gold': territory_session.gold,
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
            sess = Session.objects.get(lobby__id=lobby_id, user=request.user, active=True)

            result = get_endgame(sess)
            territories = Territory.objects.all()
            if result == "winner" or result == "loser":
                response = {'response': result}
            else:
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
                            'population': territory_session.population,
                            'army': territory_session.army,
                            'food': territory_session.food,
                            'gold': territory_session.gold,
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
    if all((request.is_ajax(), request.method == "POST", 'territory_id' in request.POST, 'lobby_id' in request.POST,
            'new_population' in request.POST, 'new_army' in request.POST)):
        territory_id = request.POST.get('territory_id')
        lobby_id = request.POST.get('lobby_id')

        if territory_id is None or lobby_id is None:
            response = 'error'
        else:
            try:
                territory_session = TerritorySession.objects.get(territory__id=territory_id, lobby__id=lobby_id)

                try:
                    new_population = int(request.POST.get('new_population'))
                except:
                    new_population = 0
                try:
                    new_army = int(request.POST.get('new_army'))
                except:
                    new_army = 0
                new_total = new_population + new_army
                old_total = territory_session.population + territory_session.army

                if new_total == old_total and territory_session.owner.user == request.user:
                    territory_session.population = new_population
                    territory_session.army = new_army
                    territory_session.save()
                    response = 'success'
                else:
                    response = 'error'
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
    if all((request.is_ajax(), request.method == 'POST', 'lobby_id' in request.POST, 't1_id' in request.POST,
            't2_id' in request.POST, 'amount' in request.POST)):
        lobby_id = request.POST.get('lobby_id')
        t1_id = request.POST.get('t1_id')
        t2_id = request.POST.get('t2_id')
        try:
            amount = int(request.POST.get('amount'))
        except:
            amount = 0

        try:
            session_1 = TerritorySession.objects.get(lobby__id=lobby_id, territory__id=t1_id)
            session_2 = TerritorySession.objects.get(lobby__id=lobby_id, territory__id=t2_id)

            if session_1.territory.name in session_2.get_borders():

                if all((session_1.army >= amount, session_1.owner.user == request.user,
                        session_2.owner.user == request.user)):
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


@login_required
def attack(request):
    """
    Attack territory 1 with the army in territory 2.
    """
    if all((request.is_ajax(), request.method == "POST", "lobby_id" in request.POST, "t1_id" in request.POST,
            "t2_id" in request.POST)):
        lobby_id = request.POST.get('lobby_id')
        t1_id = request.POST.get('t1_id')
        t2_id = request.POST.get('t2_id')

        try:
            session_1 = TerritorySession.objects.get(lobby__id=lobby_id, territory__id=t1_id)
            session_2 = TerritorySession.objects.get(lobby__id=lobby_id, territory__id=t2_id)

            if session_1.territory.name in session_2.get_borders():

                attacker = session_2.owner.user if session_2.owner is not None else ''
                defender = session_1.owner.user if session_1.owner is not None else ''

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
