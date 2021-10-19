import time
from decimal import Decimal

from bs4 import BeautifulSoup

from celery import shared_task

from currency import const
from currency import model_choices as choices
from currency.services import get_latest_rates

from django.core.cache import cache
from django.core.mail import send_mail

import requests

from settings import settings


def round_currency(num):
    return Decimal(num).quantize(Decimal('.01'))


@shared_task
def send_email(subject, full_email, recipient_list):
    recipient_list.append(settings.SUPPORT_EMAIL)
    send_mail(
        subject,
        full_email,
        settings.EMAIL_HOST,
        recipient_list,
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
                cache.delete(const.CACHE_KEY_LATEST_RATES)
                get_latest_rates()


@shared_task
def parse_monobank():

    from currency.models import Rate, Source

    source = Source.objects.get_or_create(
        code_name=const.CODE_NAME_MONOBANK,
        defaults={'name': 'MonoBank'},
    )[0]

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

    from currency.models import Rate, Source

    source = Source.objects.get_or_create(
        code_name=const.CODE_NAME_VKURSE,
        defaults={'name': 'Vkurse.ua'},
    )[0]

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

    from currency.models import Rate, Source

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


@shared_task
def parse_pumb():

    from currency.models import Rate, Source

    source = Source.objects.get_or_create(
        code_name=const.CODE_NAME_PUMB,
        defaults={'name': 'PUMB'},
    )[0]

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
        # Здесь мы получаем дочерние элементы строки таблицы в виде списка, но так как в одной из строк нет тега td,
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
                    currency_name=currency_name,
                    source=source,
                )


# @shared_task
# def parse_oschadbank():

#     from currency.models import Rate

#     source = 'oschadbank'

#     url = 'https://www.oschadbank.ua/ua'

#     available_currency_names = {
#         'USD': choices.TYPE_USD,
#         'EUR': choices.TYPE_EUR,
#     }

#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     for currency_name in available_currency_names.keys():

#         bid = soup.find('strong', {'class': f'buy-{currency_name}'}).text.strip()
#         ask = soup.find('strong', {'class': f'sell-{currency_name}'}).text.strip()
#         currency_name = available_currency_names.get(currency_name)

#         last_rate = Rate.objects.filter(
#             currency_name=currency_name,
#             source=source,
#         ).order_by('created').last()

#         if (
#             last_rate is None or
#             last_rate.bid != bid or
#             last_rate.ask != ask
#         ):

#             Rate.objects.create(
#                 ask=ask,
#                 bid=bid,
#                 currency_name=currency_name,
#                 source=source,
#             )


def days_in_year_amount(month, year):
    long_months = [1, 3, 5, 7, 8, 10, 12]
    if month in long_months:
        days = 31
    elif month == 2 and year % 4 == 0:
        days = 29
    elif month == 2:
        days = 28
    else:
        days = 30
    return days


def pretty_date(item):
    if item < 10:
        item = '0'+str(item)
    return str(item)


def parse_privatbank_archive():

    from currency.models import Rate, Source

    source = Source.objects.get_or_create(
        code_name=const.CODE_NAME_PRIVATBANK,
        defaults={'name': 'PrivatBank'},
    )[0]

    initial_time = time.time()
    initial_rates = Rate.objects.count()
    months = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    initial_year = 2020
    initial_month = 12
    years_amount = 12
    flag = False

    available_currency_types = {
        'USD': 'choices.TYPE_USD',
        'EUR': 'choices.TYPE_EUR',
    }
    amount_of_empty_days = 10

    for i in range(years_amount):

        current_year = initial_year-i
        month = initial_month

        while month in months:
            amount_of_empty_days = 10
            days = days_in_year_amount(month, current_year)

            for day in range(days, 0, -1):

                date = pretty_date(day)+'.'+pretty_date(month)+'.'+str(current_year)
                print(date)  # noqa
                url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
                response = requests.get(url)
                response.raise_for_status()
                rates = response.json()

# There is no data at some dates like 01.11.2014 so there is such check here.
# The amount of "empty" dates is determined by variable (amount_of_empty_days).
#  If in within any month quantity of 'empty' dates will be bigger that that variable, function will stop working
                if len(rates['exchangeRate']) != 0:
                    for rate in rates['exchangeRate'][1:]:

                        # At some dates like 17.05.2021 and 25.01.2021 is no field currency, so there might be exception
                        try:
                            currency_name = rate['currency']
                        except KeyError:
                            continue

                        if currency_name in available_currency_types:
                            db_date = str(current_year)+'-'+pretty_date(month)+'-'+pretty_date(day)

# At some dates like 24.08.2017 is no fields purchaseRate and saleRate, so there might be exception
                            try:
                                bid = rate['purchaseRate']
                                ask = rate['saleRate']

                                # Use this settings for parsing national bank rates
                                # bid = rate['purchaseRateNB']
                                # ask = rate['saleRateNB']
                            except KeyError:
                                continue

                            Rate.objects.update_or_create(
                                ask=ask,
                                bid=bid,
                                created=db_date,
                                currency_name=currency_name,
                                source=source,
                                defaults={'created': db_date, 'currency_name': currency_name}
                            )
                else:
                    if amount_of_empty_days == 0:
                        flag = True
                        print(f'Amount of empty days was exceeded on date {date}')  # noqa
                        break
                    print(f'An empty day was detected on date:{date}')  # noqa
                    amount_of_empty_days -= 1
                    continue

            if flag:
                break
            month -= 1

        if flag:
            break
        initial_month = 12

    print(f'Execution was finished in {time.time-initial_time} seconds. {Rate.objects.count()-initial_rates} rates was added to database')  # noqa
