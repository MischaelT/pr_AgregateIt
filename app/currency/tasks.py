from decimal import Decimal

from app.currency import const

from bs4 import BeautifulSoup

from celery import shared_task

from currency import model_choices as choices

from django.core.mail import send_mail

import requests

from settings import settings


def round_currency(num):
    return Decimal(num).quantize(Decimal('.01'))


@shared_task
def send_email(subject, full_email):
    send_mail(
        subject,
        full_email,
        settings.EMAIL_HOST,
        [settings.SUPPORT_EMAIL],
        fail_silently=False,
    )


@shared_task
def parse_privatbank():
    from currency.models import Rate, Source

    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    response.raise_for_status()

    # Мы получаем пару: обьект и запись был ли он создан

    source = Source.objects.get_or_create(
        code_name=const.CODE_NAME_PRIVATBANK,
        defaults={'name': 'PrivatBank'},
    )[0]
    rates = response.json()

    available_currency_types = {
        'USD': choices.TYPE_USD,
        'EUR': choices.TYPE_EUR,
    }

    for rate in rates:

        currency_name = rate['ccy']

        if currency_name in available_currency_types:

            bid = round_currency(rate['buy'])
            ask = round_currency(rate['sale'])

            ct = available_currency_types[currency_name]

            last_rate = Rate.objects.filter(
                currency_name=ct,
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
                    currency_name=ct,
                    source=source,
                )


@shared_task
def parse_monobank():

    from currency.models import Rate

    source = 'monobank'
    url = 'https://api.monobank.ua/bank/currency'

    response = requests.get(url)
    response.raise_for_status()

    rates = response.json()

    available_currency_codes = {
        '840': choices.TYPE_USD,
        '978': choices.TYPE_EUR,
        '980': choices.TYPE_HRN
    }

    for rate in rates:

        first_currency_code = str(rate['currencyCodeA'])
        second_currency_code = str(rate['currencyCodeB'])
        grivna_code = '980'

        if first_currency_code in available_currency_codes and second_currency_code == grivna_code:

            bid = round_currency(rate['rateBuy'])
            ask = round_currency(rate['rateSell'])

            currency_name = available_currency_codes.get(first_currency_code)

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


@shared_task
def parse_vkurse():

    from currency.models import Rate

    source = 'vkurse'
    url = 'http://vkurse.dp.ua/course.json'

    response = requests.get(url)
    json_data = response.json()

    available_currency_names = {
        'Dollar': choices.TYPE_USD,
        'Euro': choices.TYPE_EUR,
    }

    currency_names = json_data.keys()

    # currency_names представляют собой словарь, где ключами являются названия валют

    for name in currency_names:

        if name in available_currency_names:

            currency_name = available_currency_names.get(name)

            rate = json_data.get(name)
            bid = round_currency(rate['buy'])
            ask = round_currency(rate['sale'])

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


@shared_task
def parse_minfin():

    from currency.models import Rate

    source = 'minfin'

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


@shared_task
def parse_pumb():

    from currency.models import Rate

    source = 'PUMB'

    url = 'https://about.pumb.ua/ru/info/currency_converter'

    available_currency_names = {
        'USD': choices.TYPE_USD,
        'EUR': choices.TYPE_EUR,
    }

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')

    for row in table.find_all('tr'):

        col = row.find_all('td')
        # Здесь мы получаем дочерние элементы строки таблицы в виде списка, но так каr в одной из строк нет тега td,
        #  то соответствующийсписок пуст и мы не можем обратиться к его элементам по индексам
        try:
            name = col[0].text
        except IndexError:
            continue

        if name in available_currency_names:

            currency_name = available_currency_names.get(name)

            try:
                bid = col[1].text
                ask = col[2].text
            except IndexError:
                continue

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
                    currency_name=name,
                    source=source,
                )


@shared_task
def parse_oschadbank():

    from currency.models import Rate

    source = 'oschadbank'

    url = 'https://www.oschadbank.ua/ua'

    available_currency_names = {
        'USD': choices.TYPE_USD,
        'EUR': choices.TYPE_EUR,
    }

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for currency_name in available_currency_names.keys():

        bid = soup.find('strong', {'class': f'buy-{currency_name}'}).text.strip()
        ask = soup.find('strong', {'class': f'sell-{currency_name}'}).text.strip()
        currency_name = available_currency_names.get(currency_name)

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
