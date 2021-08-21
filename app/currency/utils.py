import requests
from bs4 import BeautifulSoup

url = 'https://minfin.com.ua/currency/banks/usd/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

for span in soup("span"):
    span.decompose()


result = soup.find('td', {'data-title':"Средний курс"}).text.split()
print(result)
