from django.db import models


class Rate(models.Model):
    ask = models.DecimalField(max_digits=4, decimal_places=2)
    bid = models.DecimalField(max_digits=4, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    bank_name = models.CharField(max_length=16)
    currency_name = models.CharField(max_length=3)


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=32)
    subject = models.CharField(max_length=128)
    message = models.CharField(max_length=2047)
    created = models.DateTimeField(auto_now_add=True)


class Source(models.Model):
    name = models.CharField(max_length=64)
    source_url = models.CharField(max_length=256)


# оставшиеся симфолы заменяются пробелами
