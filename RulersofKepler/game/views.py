from django.shortcuts import render

def index(request):
    return render(request, "game/index.html", {"kepler": "yess"})

def login(request):
	return render(request, "game/login.html", {})

def register(request):
	return render(request, "game/register.html", {})

def logout(request):
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