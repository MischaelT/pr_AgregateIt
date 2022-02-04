from currency.models import Rate

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help_ = 'Parse Privatbank Rate archive'

    def handle(self, *args, **options):
        print('Count: ', Rate.objects.count())  # noqa