from django.core.management.base import BaseCommand
from currency.tasks import parse_privatbank_archive


class Command(BaseCommand):
    help = 'Parse Privatbank Rate archive'

    def handle(self, *args, **options):
        parse_privatbank_archive()
