from django.urls import include, path
from rest_framework import routers

from planetarium.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
    TicketViewSet
)

app_name = "planetarium"

router = routers.DefaultRouter()

router.register(
    "show_theme",
    ShowThemeViewSet,
    basename="show_theme"
)
router.register(
    "astronomy_show",
    AstronomyShowViewSet,
    basename="astronomy_show"
)
router.register(
    "planetarium_dome",
    PlanetariumDomeViewSet,
    basename="planetarium_dome"
)
router.register(
    "show_session",
    ShowSessionViewSet,
    basename="show_session"
)
router.register(
    "reservation",
    ReservationViewSet,
    basename="reservation"
)
router.register(
    "ticket",
    TicketViewSet,
    basename="ticket"
)

urlpatterns = [path("", include(router.urls)),]
