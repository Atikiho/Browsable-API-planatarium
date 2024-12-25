from rest_framework import serializers

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_theme")

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "description": instance.description,
            "show_theme": [
                show_theme.name for show_theme in instance.show_theme.all()
            ]
        }


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row")


class ShowSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "astronomy_show": instance.astronomy_show.title,
            "planetarium_dome": instance.planetarium_dome.name,
            "show_time": instance.show_time
        }


class ShowSessionDetailSerializer(serializers.ModelSerializer):
    astronomy_show = AstronomyShowSerializer(read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(read_only=True)

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class TicketSerializer(serializers.ModelSerializer):
    show_session = ShowSessionSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "show_session",
            "reservation"
        )
