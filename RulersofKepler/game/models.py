"""
Models for the game.
"""
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class Lobby(models.Model):
    """
    Lobby model, which consists of:
    - id: auto generated by Django
    - name: a descriptive name for the lobby
    - territories: many-to-many relationship with Territory
    - sessions: many-to-many relationship with Session
    """
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    # A function to add all the territories to a lobby if not there already
    def generate_territories(self):
        for t in Territory.objects.all():
            if self.territorysession_set.filter(territory=t).count() == 0:
                TerritorySession.objects.create(territory=t, lobby=self)

    def save(self, *args, **kwargs):
        """
        Set the default lobby name.
        Note that setting a default in the field declaration would not work.
        """
        super(Lobby, self).save(*args, **kwargs)
        if self.name == "" or self.name is None:
            self.name = "Lobby " + str(self.id)
            self.save()
        self.generate_territories()


class Session(models.Model):
    """
    Game session model, which consists of:
    - id: auto generated by Django
    - active: boolean indicating whether the session is active, defaults to False
    - user: one-to-many relationship with the default Django user model
    """
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.id)+' '+self.user.username


class Territory(models.Model):
    """
    Territory model, which consists of:
    - id: auto generated by Django
    - name: the name of the territory
    - description: the description of the territory
    - owner: one-to-many relationship with Session
    - food: the amount of food produced by the territory
    - gold: the amount of gold produced by the territory
    - population: the size of the population held by the territory
    - army: the size of the army held by the territory
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250)
    food = models.IntegerField(default=100)
    gold = models.IntegerField(default=100)
    population = models.IntegerField(default=100)
    army = models.IntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "territories"



class TerritorySession(models.Model):
    """
    This will act as a de facto one-to-many relationship between Lobby and Territory
    It represents an instance of a territory in a certain game
    """
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE)
    owner = models.OneToOneField(Session, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.territory.name+' in '+self.lobby.name

    def change_owner(self, owner_session_id):
        # Change the owner of a territory in a session
        owner = Session.objects.get(id=owner_session_id)

        # Check if the owner is part of the same lobby as the
        # territory session
        if owner.lobby != self.lobby:
            raise ObjectDoesNotExist('Intended owner is not part of this lobby')

        self.owner = owner
        self.save()


# Extension to the User model
class UserProfile(models.Model):
    # link it to a User instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # games statistics
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    games_lost = models.IntegerField(default=0)
    won_percentage = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


