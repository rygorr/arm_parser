import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd


def get_by_selenium(url):
    options = webdriver.ChromeOptions()
    s = Service('C:/webdr/chromedriver.exe')
    options.add_argument('headless')
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(url)
    required_html = driver.page_source
    soup = BeautifulSoup(required_html, 'html.parser')
    return soup


def kompozit_52():
    url = 'https://kompozit52.ru/catalog/stekloplastikovaya_armatura/armatura_s_periodicheskim_profilem/'
    stekloplast = requests.get(url)
    if stekloplast.status_code != 200:
        return
    soup = BeautifulSoup(stekloplast.content, 'html.parser')
    title = soup.find_all('a', class_='row card_name')
    price = soup.find_all('div', class_='row card_price')
    title_lst, price_lst = [], []
    for t in title:
        title_lst.append(t.text.strip()[52:])
    for p in price:
        if type(p) != 'NoneType':
            price_lst.append(p.text.strip())
    for _ in range(len(title_lst)):
        title_lst[_] = f'{title_lst[_][:3]}-{title_lst[_][3:5]}'.strip()
    price_title = dict(zip(title_lst, price_lst))
    for key, value in price_title.items():
        value = value.replace('Цена: ', '')
        value = value.replace('\xa0руб.', '')
        value = value.replace(',', '.')
        if value != 'по запросу':
            price_title[key] = float(value)
    return dict(sorted(price_title.items(), key=lambda x: int(x[0][4:])))


def armatura_kompozit():
    stekloplast = requests.get('https://armaturakompozit.ru/prajs-list-armatura/')
    soup = BeautifulSoup(stekloplast.text, 'html.parser')
    table = soup.find_all('strong')
    razrab_cert = soup.find_all('b')
    table_array, r_c = [], []
    for el in table:
        if el.text == 'Равнопрочная замена металлической арматуры на стеклопластиковую':
            break
        table_array.append(el.text)
    for r in razrab_cert:
        r_c.append(r.text)
    del table_array[:6]
    table_array.insert(13, r_c[1])
    while '50' in table_array:
        table_array.remove('50')
    values, keys = [], []
    for i in range(len(table_array)):
        if i % 2 != 0:
            buf = table_array[i]
            buf = buf.replace(',', '.')
            values.append(float(buf))
        else:
            keys.append(table_array[i])
    price_list = dict(zip(keys, values))
    return price_list


def parm_nn():
    parm = requests.get('http://parmnn.ru/armatura/')
    soup = BeautifulSoup(parm.text, 'html.parser')
    my_data = soup.find_all('td')
    price_list = []
    titles, retail_price, over_1000_price, over_5000_price = [], [], [], []
    for _ in my_data:
        if _.text not in ['50-100', 'Купить', '50', 'хлыст']:
            price_list.append(_.text)
    price_list = price_list[:36]
    for _ in range(len(price_list)):
        price_list[_] = price_list[_].replace('руб.', '')
        price_list[_] = price_list[_].replace(',', '.')
    for ret in range(len(price_list)):
        if 'АСК' in price_list[ret]:
            titles.append(price_list[ret])
            retail_price.append(float(price_list[ret + 1]))
            over_1000_price.append(float(price_list[ret + 2]))
            over_5000_price.append(float(price_list[ret + 3]))
    for _ in range(len(titles)):
        titles[_] = f'АСК-{titles[_][8:10]}'.strip()
    retail = dict(zip(titles, retail_price))
    over_1000 = dict(zip(titles, over_1000_price))
    over_5000 = dict(zip(titles, over_5000_price))
    return over_5000


def armolux():
    url = 'https://armolux.ru/steklopastikovaya-armatura'
    soup = get_by_selenium(url)
    title = soup.find_all('div', class_='t778__title t-name t-name_xs js-product-name')
    price = soup.find_all('div', class_='t778__price-value js-product-price notranslate')
    title_list, price_list = [], []
    for _ in title:
        title_list.append(_.text.strip())
    for _ in price:
        price_list.append(float(_.text.replace(',', '.')))
    title_list = title_list[:11]
    price_list = price_list[:11]
    for _ in range(len(title_list)):
        title_list[_] = title_list[_][21:-3]
        title_list[_] = f'АСК-{title_list[_]}'

    price_title = dict(zip(title_list, price_list))
    return price_title


def heltex():
    url = 'https://heltex.ru/catalog/kompozitnaya-armatura/stekloplastikovaya-armatura/'
    soup = get_by_selenium(url)
    title = soup.find_all('div', class_="product-prices__name")
    price = soup.find_all('div', class_='product-prices__price')
    title_lst, price_lst = [], []
    for _ in title:
        title_lst.append(_.text[27:-2])
    for _ in price:
        p = _.text[5:20].strip()
        p = p.replace(',', '.')
        price_lst.append(float(p))
    title_price = dict(zip(title_lst, price_lst))
    return title_price


def kom_mir():
    url = 'http://kom-mir.ru/kompozitnaya-armatura#rec311796346'
    parse = get_by_selenium(url)
    title = parse.find_all('div', class_="t776__title t-name t-name_md js-product-name")
    price = parse.find_all('div', class_="t776__price-value js-product-price notranslate")
    title_lst, price_lst = [], []
    for _ in title:
        title_lst.append(f'{_.text[27:30]}-{_.text[31:33]}'.strip())
    title_lst = title_lst[:15]
    for _ in price:
        price_lst.append(_.text[3:].replace(',', '.'))
    price_lst = price_lst[:15]
    price_lst = list(map(lambda x: float(x), price_lst))
    title_price = dict(zip(title_lst, price_lst))
    return title_price


def stroy_shans():
    url = 'https://stroyshans.ru/catalog/stekloplastikovaya-kompozitnaya-armatura/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find_all('div', class_="catalog-item-property__value")
    price = soup.find_all('span', class_='catalog-item-price')
    count = 0
    title_lst, price_lst = [], []
    for _ in title:
        count += 1
        if count % 2 != 0:
            title_lst.append(f'АСК-{_.text[:2].strip()}')
    for _ in price:
        price_lst.append(float(_.text.strip()[:5].replace('a', '').strip()))
    price_title = dict(zip(title_lst, price_lst))
    return price_title


# вывод в excel файл
def equal_len_and_output():
    kom_mir_dict = kom_mir()
    kompozit_52_prices = list(kompozit_52().values())
    armatura_kompozit_prices = list(armatura_kompozit().values())
    parm_nn_prices = list(parm_nn().values())
    armolux_prices = list(armolux().values())
    stroy_shans_prices = list(stroy_shans().values())
    len_true = len(kom_mir_dict)
    while len(kompozit_52_prices) < len_true:
        kompozit_52_prices.append(None)
    while len(armatura_kompozit_prices) < len_true:
        armatura_kompozit_prices.append(None)
    while len(parm_nn_prices) < len_true:
        parm_nn_prices.append(None)
    while len(armolux_prices) < len_true:
        armolux_prices.append(None)
    while len(stroy_shans_prices) < len_true:
        stroy_shans_prices.append(None)
    table = pd.DataFrame({
        'title': kom_mir_dict.keys(),
        'Композит 52': kompozit_52_prices,
        'Арматура Композит': armatura_kompozit_prices,
        'Парм НН': parm_nn_prices,
        'Армолюкс': armolux_prices,
        'Хелтекс': heltex().values(),
        'Коммир': kom_mir_dict.values(),
        'Строй Шанс': stroy_shans_prices
    })
    table.to_excel('D:/arm_parser_out/output.xlsx')


equal_len_and_output()
