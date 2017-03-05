from django.conf.urls import url
from . import views


urlpatterns = {
    url(r'^$', views.index, name="index"),
    url(r'^login/$', views.user_login, name="login"), # change the view name bcs of conflict with Django's login()
    url(r'^register/$', views.register, name="register"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^lobby/list/$', views.lobbylist, name="lobbylist"),
    url(r'^lobby/(?P<lobbyid>[0-9]+)/join/$', views.lobbyjoin, name="lobbyjoin"),
    url(r'^lobby/create/$', views.lobbycreate, name="lobbycreate"),
    url(r'^about/$', views.about, name="about"),
    url(r'^game/(?P<gameid>[0-9]+)/$', views.game, name="game"),
    url(r'^leaderboard/$', views.leaderboard, name="leaderboard"),
    url(r'^account/(?P<accountid>[0-9]+)/view/$', views.accountview, name="accountview"),
    url(r'^account/settings/$', views.accountsettings, name="accountsettings"),
    url(r'^terms-and-conditions/$', views.termsandconditions, name="termsandconditions")
}
