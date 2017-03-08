from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def index(request):
    return render(request, "game/index.html", {"kepler": "yess"})


# changed the name because it makes a conflict with auth.login function in Django
def user_login(request):
    # if submit button was clicked on
    if request.method == 'POST':
        # obtain info from the form; get does not throw an exception
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # try to verify the user's credentials
        user = authenticate(username=username, password=password) # returns none if credentials aren't valid
        if user:
            if user.is_active: # if the user was deactivated by admins - for cheating, etc..
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rulers of Kepler account is disabled.")
        else:
            # unsuccessful authentication - tell the user so
            return render(request, 'game/login.html', {'invalid': "Invalid login details supplied."})
    else:
        return render(request, "game/login.html", {})


def register(request):
    # for template
    registered = False
    
    if request.method == 'POST':
        user_name = request.POST.get("username")
        email = request.POST.get("email")
        passwd = request.POST.get("password")

        
    else:
        return render(request, "game/register.html", {})


def user_logout(request):
    pass


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


def accountview(request):
    return render(request, "game/accountview.html", {})


def accountsettings(request):
    return render(request, "game/accountsettings.html", {})


def termsandconditions(request):
    return render(request, "game/termsandconditions.html", {})
