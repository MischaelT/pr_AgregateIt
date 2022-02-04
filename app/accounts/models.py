from django.contrib.auth.models import AbstractUser
from django.db import models


def upload_avatar(instance, filename):
    return f'avatars/{instance.id}/{filename}'


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    avatar = models.FileField(
        upload_to=upload_avatar,
        blank=True,
        null=True,
        default=None,
    )

    phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        default=None,
    )

    email = models.EmailField('email address', blank=True, unique=True)

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = ''.join(char for char in self.phone if char.isdigit())
        super().save(self, *args, **kwargs)
