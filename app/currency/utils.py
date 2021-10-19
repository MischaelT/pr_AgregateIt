# import requests

# def days_in_year_amount(month,year):
#     long_months = [1,3,5,7,8,10,12]
#     if month in long_months:
#         days = 31
#     elif month==2 and year%4==0:
#         days = 29
#     elif month == 2:
#         days =28
#     else:
#         days = 30
#     return days

# def pretty_date(item):
#     if item<10:
#         item = '0'+str(item)
#     return str(item)

# months = [12,11,10,9,8,7,6,5,4,3,2,1]
# initial_year = 2017
# initial_month = 8
# years_amount = 12
# flag = False
# available_currency_types = {
#     'USD': 'choices.TYPE_USD',
#     'EUR': 'choices.TYPE_EUR',
# }
# amount_of_empty_days=10

# for i in range(years_amount):

#     current_year = initial_year-i
#     month =initial_month

#     while month in months:
#         amount_of_empty_days=10
#         days=days_in_year_amount(month, current_year)

#         for day in range(days,0,-1):
#             day = 24
#             date = pretty_date(day)+'.'+pretty_date(month)+'.'+str(current_year)
#             print(date)
#             url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
#             response = requests.get(url)
#             response.raise_for_status()
#             rates = response.json()

#             if len(rates['exchangeRate']) != 0:
#                 for rate in rates['exchangeRate'][1:]:


#                     currency_name = rate['currency']


#                     if currency_name in available_currency_types:

#                         bid = rate['purchaseRate']
#                         ask = rate['saleRate']
#                         print(currency_name)
#                         print(bid)
#                         print(ask)
#                         print('____________________-')
#             else:
#                 if amount_of_empty_days==0:
#                     flag = True
#                     print(f'Amount of empty days was exceeded on date {date}')
#                     break
#                 print(f'An empty day was detected on date:{date}')
#                 amount_of_empty_days -= 1
#                 continue
#         if flag:
#             break
#         month -= 1

#     initial_month = 12
#     if flag:
#         break
