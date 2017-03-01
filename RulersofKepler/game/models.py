"""
Models for the game.
"""
from django.contrib.auth.models import User
from django.db import models


class Session(models.Model):
    """
    Game session model, which consists of:
    - id: auto generated by Django
    - active: boolean indicating whether the session is active, defaults to False
    - user: one-to-many relationship with the default Django user model
    """
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


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
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    owner = models.ForeignKey(Session, on_delete=models.CASCADE)
    food = models.IntegerField()
    gold = models.IntegerField()
    population = models.IntegerField()
    army = models.IntegerField()

    def __str__(self):
        return self.name


class Lobby(models.Model):
    """
    Lobby model, which consists of:
    - id: auto generated by Django
    - territories: many-to-many relationship with Territory
    - sessions: many-to-many relationship with Session
    """
    territories = models.ManyToManyField(Territory)
    sessions = models.ManyToManyField(Session)

    def __str__(self):
        return self.id
