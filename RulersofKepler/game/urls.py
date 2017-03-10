from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^lobby/list/$', views.lobbylist, name="lobbylist"),
    url(r'^lobby/(?P<lobbyid>[0-9]+)/join/$', views.lobbyjoin, name="lobbyjoin"),
    url(r'^lobby/create/$', views.lobbycreate, name="lobbycreate"),
    url(r'^about/$', views.about, name="about"),
    url(r'^game/(?P<gameid>[0-9]+)/$', views.game, name="game"),
    url(r'^leaderboard/$', views.leaderboard, name="leaderboard"),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name="profile"),
    url(r'^terms-and-conditions/$', views.termsandconditions, name="termsandconditions")
]
