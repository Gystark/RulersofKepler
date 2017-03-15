from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from .models import Lobby, Session, Territory, TerritorySession
from .forms import LobbyCreationForm

# The maximum number of sessions that can join a lobby
MAX_SESSIONS = 4


def index(request):
    return render(request, "game/index.html", {})


def lobbylist(request):
    """
    List all lobbies which have less than the maximum number of players.
    """
    lobbies = Lobby.objects.all().exclude(Q(session__user__username=request.user.username) | Q(session=MAX_SESSIONS))
    return render(request, "game/lobbylist.html", {'lobbies': lobbies, "max_sessions": MAX_SESSIONS})


def lobbyjoin(request, lobby_id):
    """
    Join the lobby specified by lobby_id
    """
    try:
        lobby = Lobby.objects.get(id=lobby_id)

        if lobby.session_set.filter(user=request.user).count() != 0:
            return redirect('game', gameid=lobby.id)

        Session.objects.create(user=request.user, lobby=lobby)
        return redirect('game', gameid=lobby.id)
    except Lobby.ObjectDoesNotExist:
        messages.error(request, 'Error joining the lobby, please try again.')
        return redirect('lobbylist')


def lobbycreate(request):
    """
    Create a new lobby.
    """
    if request.method == "POST":
        form = LobbyCreationForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated():
                lobby = Lobby.objects.create(name=form.cleaned_data.get("name"))

                return redirect('lobbyjoin', lobby_id=lobby.id)
            else:
                messages.error(request, "You mus be logged in to create a lobby.")
                return redirect('index')
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


def game(request, gameid):
    return render(request, "game/game.html", {})


def leaderboard(request):
    """
    Compute and return the top 10 players.
    """
    # TODO replace the dummy values when we've decided on scoring
    if request.user.is_authenticated():
        stats = []
        users = User.objects.all()
        for user in users:
            magic_value = Session.objects.filter(user=user).count()
            stats.append({"name": user.username, "wins": magic_value, "losses": magic_value, "ratio": magic_value})
        return render(request, "game/leaderboard.html", {"stats": stats})
    else:
        messages.error(request, "You must be logged in to view the leaderboard.")
        return redirect('index')


class ProfileView(LoginRequiredMixin, DetailView):
    """
    View the current user's profile
    """
    model = User
    template_name = "game/profile.html"
    permission_denied_message = "Please log in to view your profile"
    raise_exception = True


def accountview(request, accountid):
    return render(request, "game/profile.html", {})


def termsandconditions(request):
    return render(request, "game/terms.html", {})
