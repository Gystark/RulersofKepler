from django.contrib import admin
from game.models import Territory, Lobby, Session, TerritorySession

admin.site.register(Territory)
admin.site.register(Lobby)
admin.site.register(Session)
admin.site.register(TerritorySession)
