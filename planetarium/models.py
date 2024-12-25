from django.contrib.auth import get_user_model
from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    show_theme = models.ManyToManyField(
        to=ShowTheme,
        related_name="astronomy_shows"
    )

    def __str__(self):
        return self.title


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        to=AstronomyShow,
        on_delete=models.CASCADE,
        related_name="show_session"
    )
    planetarium_dome = models.ForeignKey(
        to=PlanetariumDome,
        on_delete=models.CASCADE,
        related_name="show_session"
    )
    show_time = models.DateTimeField()


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="reservations",
    )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        to=ShowSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        to=Reservation,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "show_session"],
                name="unique_row_seat_show_session"
            )
        ]
