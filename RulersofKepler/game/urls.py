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
    url(r'^game-won/$', views.gamewon, name="gamewon"),
    url(r'^game-over/$', views.gameover, name="gameover"),

    # Ajax urls
    url(r'game-ajax/(?P<lobby_id>[0-9]+)/territory/get-all', views.get_territory_all, name="get_territory_all"),
    url(r'game-ajax/(?P<lobby_id>[0-9]+)/territory/get-reduced', views.get_territory_reduced,
        name="get_territory_reduced"),
    url(r'^game-ajax/territory/set-population-army/$', views.set_population_army, name="set_population_army"),
    url(r'^game-ajax/army/move/$', views.move_army, name='move_army'),
    url(r'^game-ajax/army/attack/$', views.attack, name="attack"),
    url(r'^game-ajax/resign/$', views.resign, name="resign")
]
