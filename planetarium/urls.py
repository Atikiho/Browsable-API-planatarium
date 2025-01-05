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
    "show-themes",
    ShowThemeViewSet,
    basename="show-themes"
)
router.register(
    "astronomy-shows",
    AstronomyShowViewSet,
    basename="astronomy-shows"
)
router.register(
    "planetarium-domes",
    PlanetariumDomeViewSet,
    basename="planetarium-domes"
)
router.register(
    "show-sessions",
    ShowSessionViewSet,
    basename="show-sessions"
)
router.register(
    "reservations",
    ReservationViewSet,
    basename="reservations"
)
router.register(
    "tickets",
    TicketViewSet,
    basename="tickets"
)

urlpatterns = router.urls
