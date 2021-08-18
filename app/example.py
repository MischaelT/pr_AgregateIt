# import requests
# from bs4 import BeautifulSoup

# url = 'https://alfabank.ua/ru'

# response = requests.get(url)

# response.raise_for_status()

# soup = BeautifulSoup(response.text, 'html.parser')

# # strip убирает все лишние теги рядом с результатом
# soup.find_all('span', {'data-currency':'USD_BUY'}).text.strip()


# def parse_vkurse():
#     import requests
#     from bs4 import BeautifulSoup

#     url = 'http://vkurse.dp.ua/'

#     content = requests.get(url)

#     content.raise_for_status()

#     soup = BeautifulSoup(content.text, 'html.parser')

#     print(soup.find_all('div',{'class':"pokupka-section"}))

# parse_vkurse()

from decimal import Decimal


def round_currency(num):
    return Decimal(num).quantize(Decimal('.01'))



import requests

url = 'https://api.monobank.ua/bank/currency'
response = requests.get(url)
response.raise_for_status()

source = 'monobank'
rates = response.json()
available_currency_codes = {'840':'USD', '978':'EUR'}

# print(rates)

for rate in rates:

    first_currency_code = str(rate['currencyCodeA'])
    # isRateCross = lambda x: True if (x!='rateCross') else False
    # value = str(rate['rateCross'])
    # cross_rate = rate.get('rateCross')
    second_currency_code = str(rate['currencyCodeB'])
    grivna_code = '980'

    if (first_currency_code in available_currency_codes.keys() and second_currency_code == grivna_code):

        ask = round_currency(rate['rateSell'])
        bid = round_currency(rate['rateBuy'])
        print(ask)
        print(bid)
        last_rate = Rate.objects.filter(
            currency_name=dict.get('currency_code'),
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