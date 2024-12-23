from django.contrib.auth import get_user_model
from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        to=AstronomyShow,
        on_delete=models.CASCADE
    )
    planetarium_dome = models.ForeignKey(
        to=PlanetariumDome,
        on_delete=models.CASCADE
    )
    show_time = models.DateTimeField()


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = get_user_model()


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        to=ShowSession,
        on_delete=models.CASCADE
    )
    reservation = models.ForeignKey(
        to=Reservation,
        on_delete=models.DO_NOTHING
    )
