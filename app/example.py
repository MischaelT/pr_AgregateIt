# import requests
# from bs4 import BeautifulSoup

# url = 'https://alfabank.ua/ru'

# response = requests.get(url)

# response.raise_for_status()

# soup = BeautifulSoup(response.text, 'html.parser')

# # strip убирает все лишние теги рядом с результатом
# soup.find_all('span', {'data-currency':'USD_BUY'}).text.strip()


def parse_vkurse():
    import requests
    from bs4 import BeautifulSoup

    url = 'http://vkurse.dp.ua/'

    content = requests.get(url)

    content.raise_for_status()

    soup = BeautifulSoup(content.text, 'html.parser')

    print(soup.find_all('div',{'class':"pokupka-section"}))

parse_vkurse()