from currency.tasks import parse_privatbank_archive

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help_ = 'Parse Privatbank Rate archive'

    def handle(self, *args, **options):
        parse_privatbank_archive()
