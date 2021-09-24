from django.db.models.deletion import SET_NULL
from currency import model_choices as choices

from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=64)
    code_name = models.CharField(max_length=24, unique=True, editable=False)
    source_url = models.CharField(max_length=256)


class Rate(models.Model):
    ask = models.DecimalField(max_digits=4, decimal_places=2)
    bid = models.DecimalField(max_digits=4, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    currency_name = models.CharField(
        max_length=3,
        choices=choices.RATE_TYPES,
        blank=False,
        null=False,
        default=choices.TYPE_USD,
    )
    source = models.ForeignKey(
        Source,
        related_name='rates',
        on_delete=models.CASCADE,
    )
    currency_type = models.CharField(max_length=8)


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=32)
    subject = models.CharField(max_length=128)
    message = models.CharField(max_length=2047)
    created = models.DateTimeField(auto_now_add=True)


class ResponseLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status_code = models.PositiveSmallIntegerField()
    path = models.CharField(max_length=255)
    response_time = models.PositiveSmallIntegerField(
        help_text='in milliseconds'
    )
    request_method = models.CharField(max_length=8, choices=choices.RESPONCE_LOG_TYPES)

# оставшиеся симфолы заменяются пробелами
