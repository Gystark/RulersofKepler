from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^lobby/list/$', views.lobbylist, name="lobbylist"),
    url(r'^lobby/(?P<lobby_id>[0-9]+)/join/$', views.lobbyjoin, name="lobbyjoin"),
    url(r'^lobby/create/$', views.lobbycreate, name="lobbycreate"),
    url(r'^about/$', views.about, name="about"),
    url(r'^game/(?P<lobby_id>[0-9]+)/$', views.game, name="game"),
    url(r'^leaderboard/$', views.leaderboard, name="leaderboard"),
    url(r'^profile/(?P<username>[\w]+)/$', views.profile, name="profile"),
    url(r'^terms-and-conditions/$', views.termsandconditions, name="termsandconditions"),

    url(r'^game-ajax/(?P<lobby_id>[0-9]+)/territory/(?P<territory_id>[0-9]+)/data/$', views.get_territory_data, name="get_territory_data")
]
