from decimal import Decimal

from currency import const

from bs4 import BeautifulSoup

from celery import shared_task

from currency import model_choices as choices

from django.core.mail import send_mail

import requests

from settings import settings


def round_currency(num):
    return Decimal(num).quantize(Decimal('.01'))



def parse_minfin():

    from models import Rate, Source

    source = Source.objects.get_or_create(
        code_name=const.CODE_NAME_MINFIN,
        defaults={'name': 'MinFin'},
    )[0]

    urls = {
        choices.TYPE_USD: 'https://minfin.com.ua/currency/banks/usd/',
        choices.TYPE_EUR: 'https://minfin.com.ua/currency/banks/eur/',
        }

    for currency_name in urls:

        response = requests.get(urls.get(currency_name))
        soup = BeautifulSoup(response.text, 'html.parser')

        for span in soup("span"):
            span.decompose()

        # Получаем список, где первое значение - это покупка, а второе - продажа
        result = soup.find('td', {'data-title': "Средний курс"}).text.split()
        bid = round_currency(result[0])
        ask = round_currency(result[1])

        last_rate = Rate.objects.filter(
            currency_name=currency_name,
            source=source,
        ).order_by('created').last()

        if (
            last_rate is None or
            last_rate.bid != bid or
            last_rate.ask != ask
        ):

            Rate.objects.create(
                ask=ask,
                bid=bid,
                currency_name=currency_name,
                source=source,
            )

parse_minfin()