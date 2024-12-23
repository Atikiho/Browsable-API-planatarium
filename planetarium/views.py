from rest_framework import viewsets

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ReservationSerializer,
    TicketSerializer,
    ShowSessionDetailSerializer
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    serializer_class = ShowThemeSerializer
    queryset = ShowTheme.objects.all()


class AstronomyShowViewSet(viewsets.ModelViewSet):
    serializer_class = AstronomyShowSerializer
    queryset = AstronomyShow.objects.all()


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    serializer_class = PlanetariumDomeSerializer
    queryset = PlanetariumDome.objects.all()


class ShowSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ShowSessionSerializer
    queryset = ShowSession.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionSerializer
        elif self.action == "retrieve":
            return ShowSessionDetailSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
