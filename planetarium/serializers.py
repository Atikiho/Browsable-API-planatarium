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
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


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
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class TicketSerializer(serializers.ModelSerializer):
    show_session = ShowSessionSerializer()
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

    def validate(self, attrs):
        row = attrs.get("row")
        seat = attrs.get("seat")
        show_session_data = attrs.get("show_session")

        max_rows = show_session_data["planetarium_dome"].rows
        max_seat = show_session_data["planetarium_dome"].seats_in_row

        if row > max_rows or seat > max_seat:
            raise serializers.ValidationError(f"row should be less than {max_rows} "
                                              f"and seat should be less than {max_seat}")

        if row < 0 or seat < 0:
            raise serializers.ValidationError("row and seat can't be negative")

        show_session = ShowSession.objects.filter(**show_session_data).first()

        if Ticket.objects.filter(row=row, seat=seat, show_session=show_session).exists():
            raise serializers.ValidationError("This place is already taken!")

        return attrs

    def create(self, validated_data):
        show_session_data = validated_data.pop("show_session")
        request_user = self.context['request'].user

        show_session, _ = ShowSession.objects.get_or_create(**show_session_data)

        reservation = Reservation.objects.create(user=request_user)

        ticket = Ticket.objects.create(
            **validated_data,
            show_session=show_session,
            reservation=reservation
        )
        return ticket
