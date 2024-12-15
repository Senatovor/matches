from bs4 import BeautifulSoup
import requests


def parsing_prices(url: str):
    tables = []
    table = []
    price_array = []
    prices_array = []

    request = requests.get(url)
    html_content = request.content
    soup = BeautifulSoup(html_content, 'html.parser')

    for data in soup.find_all('div', class_='ma-accordion-tab-content'):
        tables.append(data)

    for data in tables:
        if data.find_all('tr'):
            prices = data.find_all('tr')
            for price in prices:
                price_array.append(price.text.split())
            table.append(price_array)
            price_array = []

    for prices in table:
        price_array = []

        for price in prices[1:-1]:
            if len(price) == 1:
                number = price[0][1:].lstrip('0')
                pair = [price[0].replace(number, ''), number]
                price_array.append([int(pair[0]), float(pair[1])])
            else:
                price_array.append([int(price[0]), float(price[1])])

        prices_array.append(price_array)

    return prices_array


def parsing_math(url: str):
    tables = []
    names_and_descriptions = []

    request = requests.get(url)
    html_content = request.content
    soup = BeautifulSoup(html_content, 'html.parser')
    for data in soup.find_all('div', class_='elementor-image-box-wrapper'):
        tables.append(data)

    math = soup.find_all('h5')
    description = soup.find_all('p', class_='elementor-image-box-description')

    if len(math) == len(description):
        start = 0
    else:
        start = 1

    for i, j in zip(math, description[start:]):
        names_and_descriptions.append([i.text, j.text.replace('\n', ' ')])  # Если нужны \n -> убираем replace

    return names_and_descriptions
