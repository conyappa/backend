from django.db.models import signals
from django.dispatch import receiver

from lottery.models import Draw

from .models import User


@receiver(signal=signals.post_save, sender=User)
def user_join_current_draw(sender, instance, created, *args, **kwargs):
    if created and Draw.objects.exists():
        draw = Draw.objects.ongoing()
        draw.add_tickets(user=instance, n=instance.number_of_tickets)
