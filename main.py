import requests
from bs4 import BeautifulSoup


def kompozit_52():
    stekloplast = \
        requests.get("https://kompozit52.ru/catalog/stekloplastikovaya_armatura/armatura_s_periodicheskim_profilem/")
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
    price_title = dict(zip(title_lst, price_lst))
    for key, value in price_title.items():
        value = value.replace('Цена: ', '')
        value = value.replace('\xa0руб.', '')
        value = value.replace(',', '.')
        if value != 'по запросу':
            price_title[key] = float(value)
    return price_title


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
    retail = dict(zip(titles, retail_price))
    over_1000 = dict(zip(titles, over_1000_price))
    over_5000 = dict(zip(titles, over_5000_price))
    return retail, over_1000, over_5000


# пока что вывод всех словарей
print(kompozit_52())
print(armatura_kompozit())
print(parm_nn())

