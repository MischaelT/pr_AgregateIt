from django.core.management.base import BaseCommand, CommandError
from currency.models import Rate


class Command(BaseCommand):
    help = 'Parse Privatbank Rate archive'

    def handle(self, *args, **options):
        print('Count: ', Rate.objects.count())