from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import DetailView


def index(request):
    return render(request, "game/index.html", {"kepler": "yess"})


def lobbylist(request):
    return render(request, "game/lobbylist.html", {})


def lobbyjoin(request):
    pass


def lobbycreate(request):
    return render(request, "game/lobbycreate.html", {})


def about(request):
    return render(request, "game/about.html", {})


def game(request):
    return render(request, "game/game.html", {})


def leaderboard(request):
    return render(request, "game/leaderboard.html", {})


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
    return render(request, "game/termsandconditions.html", {})
