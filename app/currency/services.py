from currency import const
from currency import model_choices as mch
from currency.models import Rate, Source

from django.core.cache import cache


def get_latest_rates():
    '''

        function for getting latest rates from cache

        privatbank - USD
        privatbank - EUR
        monobank - USD
        monobank - EUR
    '''

    latest_rates = cache.get(const.CACHE_KEY_LATEST_RATES)
    if latest_rates is not None:
        return latest_rates

    rates = []
    for source in Source.objects.all():
        for currency_type, _ in mch.RATE_TYPES:

            rate = Rate.objects \
                .filter(source=source, currency_name=currency_type) \
                .order_by('-created').first()

            if rate is not None:
                rates.append(rate)

    cache.set(const.CACHE_KEY_LATEST_RATES, rates, 60 * 60 * 24 * 14)

    return rates
