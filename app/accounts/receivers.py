import uuid

from accounts.models import User

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def update(sender, instance, **kwargs):
    if instance.phone:
        instance.phone = ''.join(char for char in instance.phone if char.isdigit())


@receiver(post_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = str(uuid.uuid4())
