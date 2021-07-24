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
    message = models.TextField()

# оставшиеся симфолы заменяются пробелами
