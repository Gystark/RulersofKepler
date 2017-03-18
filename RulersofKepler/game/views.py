from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
        sess = Session.objects.get(user=request.user, active=True)
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
def get_territory_data(request, lobby_id, territory_id):
    if request.is_ajax() and request.method == 'GET':
        lobby = Lobby.objects.get(id=lobby_id)

        territory = Territory.objects.get(id=territory_id)

        territory_session = TerritorySession.objects.get(territory=territory, lobby=lobby)

        owner = territory_session.owner.username if territory_session.owner is not None else ''

        return JsonResponse({
            'name': territory.name,
            'description': territory.description,
            'population': territory_session.population,
            'army': territory_session.army,
            'food': territory.food,
            'gold': territory.gold,
            'owner': owner
        })

    messages.error(request, 'System error, please try again.')
    return redirect('index')
