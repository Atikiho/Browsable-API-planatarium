from django.db.models.signals import post_delete
from django.dispatch import receiver

from planetarium.models import Ticket


@receiver(post_delete, sender=Ticket)
def delete_reservation_if_no_tickets(sender, instance, **kwargs):
    reservation = instance.reservation

    if not reservation.tickets.exists():
        reservation.delete()
