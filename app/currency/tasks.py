
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.mail import send_mail
from settings import settings
from celery import shared_task
from decimal import Decimal
from currency import model_choices as choices

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
    import requests
    from currency.models import Rate

    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    response.raise_for_status()

    source = 'privatbank'
    rates = response.json()

    available_currency_types = {
        'USD': choices.TYPE_USD,
        'EUR': choices.TYPE_EUR,
    }

    for rate in rates:

        currency_name =  rate['ccy']

        if currency_name in available_currency_types:

            ask = round_currency(rate['sale'])
            bid = round_currency(rate['buy'])
            ct = available_currency_types[currency_name]

            last_rate = Rate.objects.filter(
                currency_name=ct,
                bank_name=source,
            ).order_by('created').last()

            if (
                last_rate is None or
                last_rate.bid != bid or
                last_rate.ask != ask
            ):

                Rate.objects.create(
                    ask=bid,
                    bid=ask,
                    currency_name=ct,
                    bank_name = source,
                )

@shared_task
def parse_monobank():

    import requests
    from currency.models import Rate

    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    response.raise_for_status()

    source = 'monobank'
    rates = response.json()
    available_currency_codes = {'840':'USD', '978':'EUR'}

    for rate in rates:

        first_currency_code = str(rate['currencyCodeA'])
        second_currency_code = str(rate['currencyCodeB'])
        grivna_code = '980'

        if first_currency_code in available_currency_codes.keys() and second_currency_code == grivna_code:

            ask = round_currency(rate['rateSell'])
            bid = round_currency(rate['rateBuy'])
            currency_name = available_currency_codes.get(first_currency_code)

            last_rate = Rate.objects.filter(
                currency_name= currency_name,
                bank_name=source,
            ).order_by('created').last()

            if (
                last_rate is None or
                last_rate.bid != bid or
                last_rate.ask != ask
            ):

                Rate.objects.create(
                    ask=bid,
                    bid=ask,
                    currency_name=currency_name,
                    bank_name = source,
                )

@shared_task
def parse_vkurse():
    import requests
    from currency.models import Rate

    url = 'http://vkurse.dp.ua/course.json'

    response = requests.get(url)
    json_data = response.json()
    source = 'vkurse'
    available_currency_types = ('Dollar', 'Euro')
    currency_names =  json_data.keys()

    for name in currency_names:

        if name in available_currency_types:
            rate = json_data.get(name)
            ask = round_currency(rate['sale'])
            bid = round_currency(rate['buy'])

            last_rate = Rate.objects.filter(
                currency_name=name,
                bank_name=source,
            ).order_by('created').last()

            if (
                last_rate is None or
                last_rate.bid != bid or
                last_rate.ask != ask
            ):

                Rate.objects.create(
                    ask=bid,
                    bid=ask,
                    currency_name=name,
                    bank_name = source,
                )



@shared_task
def parse_minfin():
    import requests
    from bs4 import BeautifulSoup

    url = 'https://minfin.com.ua/currency/banks/usd/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    for span in soup("span"):
        span.decompose()


    result = soup.find('td', {'data-title':"Средний курс"}).text.split()
    print(result)

@shared_task
def parse_CMC():
    pass

def parse_TradingView():
    pass