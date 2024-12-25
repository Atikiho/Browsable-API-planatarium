from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = AstronomyShow.objects.prefetch_related("show_theme")
        show_theme = self.request.query_params.get("show_theme", "").strip()

        if show_theme:
            show_themes = [int(str_id) for str_id in show_theme.split(",")]
            queryset = queryset.filter(show_theme__id__in=show_themes)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "show_theme",
                type={"type": "list", "items": {"type": "number"}},
                description="search by show_theme id's"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    serializer_class = PlanetariumDomeSerializer
    queryset = PlanetariumDome.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.select_related("astronomy_show", "planetarium_dome")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionSerializer
        elif self.action == "retrieve":
            return ShowSessionDetailSerializer
        return ShowSessionSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.select_related("user")
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
