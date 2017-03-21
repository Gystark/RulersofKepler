"""
Models for the game.
"""
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from random import randrange
import json


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

    class Meta:
        verbose_name_plural = "lobbies"

    # A function to add all the territories to a lobby if not there already
    def generate_territories(self):
        for t in Territory.objects.all():
            if self.territorysession_set.filter(territory=t).count() == 0:
                TerritorySession.objects.create(territory=t, lobby=self, population=t.default_population,
                                                army=t.default_army)

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
    colour = models.CharField(max_length=20, default='')

    def __str__(self):
        return str(self.id) + ' ' + self.user.username

    def save(self, *args, **kwargs):
        super(Session, self).save(*args, **kwargs)
        if self.colour == '' or self.colour is None:
            r = randrange(0, 255)
            g = randrange(0, 255)
            b = randrange(0, 255)
            self.colour = '['+str(r)+', '+str(g)+', '+str(b)+']'
            self.save()

    def get_colour(self):
        return json.loads(self.colour)

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
    - borders: many to many relationship to self - neighbouring territorries
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=2502)
    food = models.IntegerField(default=100)
    gold = models.IntegerField(default=100)
    default_population = models.IntegerField(default=100)
    default_army = models.IntegerField(default=100)
    coordinates = models.TextField(max_length=500,default="")
    borders = models.ManyToManyField('self')

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
    owner = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    population = models.IntegerField(default=100)
    army = models.IntegerField(default=100)

    def __str__(self):
        return self.territory.name + ' in ' + self.lobby.name

    # Return borders as a list
    def get_borders(self):
        borders = []
        for t in self.territory.borders.all():
            borders.append(t.name)
        return borders

    def change_owner(self, owner):
        # Change the owner of a territory in a session

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

    def __str__(self):
        return self.user.username
