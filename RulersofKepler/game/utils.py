from random import randrange, uniform
from math import ceil

from .models import TerritorySession, UserProfile, Session


def get_initial_territory(lobby):
    """
    Get a random territory that doesn't have an owner
    """
    if TerritorySession.objects.filter(lobby=lobby, owner=None).count() == 0:
        return False
    while True:
        terr_id = randrange(1, 19)
        ts = TerritorySession.objects.get(lobby=lobby, territory__id=terr_id)
        if not ts.owner:
            return ts


def get_user_games_lost(userprofile):
    """
    Return the number of games lost by the given user. 
    """
    return userprofile.games_played - userprofile.games_won


def get_user_win_percentage(userprofile):
    """
    Return the win/loss ratio of the given user.
    """
    try:
        percentage = 100.0 * userprofile.games_won / userprofile.games_played
    except ZeroDivisionError:
        percentage = 0.0
    # get only 2 digits after the decimal point
    return ceil(percentage * 100.0) / 100.0


def get_battle_winner(defend_terr, attack_terr):
    """
    Get the winner in a battle between two territories
    Also change the territory owner accordingly
    """
    def_score = (defend_terr.army * 1.0 + 0.15 * (
        defend_terr.food + defend_terr.gold) + 0.1 * defend_terr.population) * uniform(0.9, 1.1)
    att_score = (attack_terr.army * 1.0 + 0.15 * (
        attack_terr.food + attack_terr.gold) + 0.1 * attack_terr.population) * uniform(0.9, 1.1)
    if att_score > def_score:
        defend_terr.change_owner(attack_terr.owner)
        defend_terr.army /= 2
        defend_terr.food *= 0.9
        defend_terr.gold *= 0.85
        attack_terr.army *= uniform(0.9, 1.0)
        attack_terr.save()
        defend_terr.save()
        return attack_terr.owner.user
    attack_terr.army /= 2
    defend_terr.food *= 0.85
    defend_terr.gold *= 0.83
    attack_terr.save()
    defend_terr.save()
    if defend_terr.owner != '' and defend_terr.owner is not None:
        return defend_terr.owner.user
    else:
        return ''


def get_endgame(session):
    """
    Handle the end of a game.
    """
    terr = TerritorySession.objects.filter(owner=session).count()
    if terr == 0:
        session.active = False
        session.save()

        return 'loser'
    elif terr == 19:
        session.active = False
        session.save()

        score_game(session)

        session.lobby.active = False
        session.lobby.save()

        return 'winner'
    return False


def score_game(session):
    """
    Increase the number of games played and won when a game has ended.
    """
    # Give score to the winner
    winner_profile = UserProfile.objects.get_or_create(user=session.user)[0]
    winner_profile.games_played += 1
    winner_profile.games_won += 1
    winner_profile.save()

    # Give score to the losers
    for loser in Session.objects.filter(lobby=session.lobby).exclude(id=session.id):
        loser_profile = UserProfile.objects.get_or_create(user=loser.user)[0]

        loser_profile.games_played += 1
        loser_profile.save()

