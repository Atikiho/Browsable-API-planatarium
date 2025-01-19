from parameterized import parameterized
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Ticket, Reservation
)
from planetarium.serializers import AstronomyShowSerializer


class PlanetariumTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            username="test",
            password="test",
        )
        self.user2 = get_user_model().objects.create_user(
            email="test2@test.com",
            username="test2",
            password="test2",
        )
        self.admin = get_user_model().objects.create_superuser(
            email="test_admin@test.com",
            username="test_admin",
            password="test",
        )
        self.admin.is_staff = True
        for i in range(0, 3):
            show_theme = ShowTheme.objects.create(name=f"Test{i}")
            astronomy_show = AstronomyShow.objects.create(
                title=f"Test{i}",
                description=f"Created especially for test{i}",
            )
            astronomy_show.show_theme.add(show_theme)

            planetarium_dome = PlanetariumDome.objects.create(
                name=f"Test{i}",
                rows=i + 3,
                seats_in_row=i + 3,
            )

            show_session = ShowSession.objects.create(
                show_time="2024-12-25T19:37:00Z",
                astronomy_show=astronomy_show,
                planetarium_dome=planetarium_dome
            )
            reservation = Reservation.objects.create(
                user=self.user
            )
            Ticket.objects.create(
                row=i,
                seat=i,
                show_session=show_session,
                reservation=reservation,
            )


    @parameterized.expand([
        ("GET", "planetarium:show-sessions", status.HTTP_401_UNAUTHORIZED),
        ("POST", "planetarium:show-sessions", status.HTTP_401_UNAUTHORIZED),
        ("DELETE", "planetarium:show-sessions", status.HTTP_401_UNAUTHORIZED),
        ("GET", "planetarium:show-themes", status.HTTP_401_UNAUTHORIZED),
        ("POST", "planetarium:show-themes", status.HTTP_401_UNAUTHORIZED),
        ("DELETE", "planetarium:show-themes", status.HTTP_401_UNAUTHORIZED),
        ("GET", "planetarium:astronomy-shows", status.HTTP_401_UNAUTHORIZED),
        ("POST", "planetarium:astronomy-shows", status.HTTP_401_UNAUTHORIZED),
        ("DELETE", "planetarium:astronomy-shows", status.HTTP_401_UNAUTHORIZED),
        ("GET", "planetarium:planetarium-domes", status.HTTP_401_UNAUTHORIZED),
        ("POST", "planetarium:planetarium-domes", status.HTTP_401_UNAUTHORIZED),
        ("DELETE", "planetarium:planetarium-domes", status.HTTP_401_UNAUTHORIZED),
    ])
    def test_anonym_access(self, method, url, expected_status):
        res = getattr(self.client, method.lower())(reverse(f"{url}-list"))
        self.assertEqual(res.status_code, expected_status)

    @parameterized.expand([
        ("GET", "planetarium:show-sessions", status.HTTP_200_OK),
        ("POST", "planetarium:show-sessions", status.HTTP_403_FORBIDDEN),
        ("DELETE", "planetarium:show-sessions", status.HTTP_403_FORBIDDEN),
        ("GET", "planetarium:show-themes", status.HTTP_200_OK),
        ("POST", "planetarium:show-themes", status.HTTP_403_FORBIDDEN),
        ("DELETE", "planetarium:show-themes", status.HTTP_403_FORBIDDEN),
        ("GET", "planetarium:astronomy-shows", status.HTTP_200_OK),
        ("POST", "planetarium:astronomy-shows", status.HTTP_403_FORBIDDEN),
        ("DELETE", "planetarium:astronomy-shows", status.HTTP_403_FORBIDDEN),
        ("GET", "planetarium:planetarium-domes", status.HTTP_200_OK),
        ("POST", "planetarium:planetarium-domes", status.HTTP_403_FORBIDDEN),
        ("DELETE", "planetarium:planetarium-domes", status.HTTP_403_FORBIDDEN),
    ])
    def test_authorized_user_access(self, method, url, expected_status):
        self.client.force_authenticate(user=self.user)

        res = getattr(self.client, method.lower())(reverse(f"{url}-list"))
        self.assertEqual(res.status_code, expected_status)


    @parameterized.expand([
        ("GET", "planetarium:show-sessions", status.HTTP_200_OK),
        ("POST", "planetarium:show-sessions", status.HTTP_400_BAD_REQUEST),
        ("GET", "planetarium:show-themes", status.HTTP_200_OK),
        ("POST", "planetarium:show-themes", status.HTTP_400_BAD_REQUEST),
        ("GET", "planetarium:astronomy-shows", status.HTTP_200_OK),
        ("POST", "planetarium:astronomy-shows", status.HTTP_400_BAD_REQUEST),
        ("GET", "planetarium:planetarium-domes", status.HTTP_200_OK),
        ("POST", "planetarium:planetarium-domes", status.HTTP_400_BAD_REQUEST),
    ])
    def test_admin_user_access(self, method, url, expected_status):
        self.client.force_authenticate(user=self.admin)
        res = getattr(self.client, method.lower())(reverse(f"{url}-list"))

        self.assertEqual(res.status_code, expected_status)

    @parameterized.expand(
        [
            "planetarium:show-sessions",
            "planetarium:show-themes",
            "planetarium:astronomy-shows",
            "planetarium:planetarium-domes"
        ]
    )
    def test_admin_user_deletion(self, url):
        self.client.force_authenticate(user=self.admin)
        res = self.client.delete(reverse(f"{url}-detail", args=[1]))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_ticket_validation(self):
        self.client.force_authenticate(user=self.user)
        ticket_data = {
            "row": 2,
            "seat": 3,
            "show_session_id": 1,
            "reservation": 1,
        }

        res = self.client.post(reverse("planetarium:tickets-list"), ticket_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        ticket_data["row"] = 1000

        res = self.client.post(reverse("planetarium:tickets-list"), ticket_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        ticket_data["row"] = 1
        ticket_data["seat"] = 1000

        res = self.client.post(reverse("planetarium:tickets-list"), ticket_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        ticket_data["row"] = -12
        ticket_data["seat"] = -352

        res = self.client.post(reverse("planetarium:tickets-list"), ticket_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @parameterized.expand(
        [
            ("user2", status.HTTP_403_FORBIDDEN, 1),
            ("user", status.HTTP_204_NO_CONTENT, 1),
            ("admin", status.HTTP_204_NO_CONTENT, 2)
        ]
    )
    def test_ticket_deleting(self, user, status_code, ticket_id):
        self.client.force_authenticate(user=getattr(self, user))
        res = self.client.delete(
            reverse("planetarium:tickets-detail", args=(ticket_id,))
        )
        self.assertEqual(res.status_code, status_code)

    def test_reservation_deletion_on_ticket_deletion(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(
            reverse("planetarium:tickets-detail", args=[1])
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Ticket.objects.filter(id=1).exists())
        self.assertFalse(Reservation.objects.filter(id=1).exists())

    def test_filtering(self):
        self.client.force_authenticate(user=self.user)

        res = self.client.get(
            reverse("planetarium:astronomy-shows-list"),
            data={"show_theme": "1, 2"}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = AstronomyShowSerializer(
            AstronomyShow.objects.filter(show_theme__id__in=[1, 2]),
            many=True
        )

        self.assertEqual(res.data, serializer.data)
