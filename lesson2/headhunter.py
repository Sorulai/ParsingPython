import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas


def correct_price(my_str, sub_string):
    my_str = my_str.replace(sub_string, '')
    my_str = my_str.split(' ')
    if len(my_str) > 2:
        my_str.pop(1)
        return int(my_str[0].replace('\u202f', '')), int(my_str[1].replace('\u202f', '')), my_str[2]
    else:
        return int(my_str[0].replace('\u202f', '')), my_str[1]


user_text = input('Введите название вакансии: ')

url = 'https://hh.ru'
full_url = 'https://hh.ru/search/vacancy'
params = {
    'text': user_text,
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

vacancies_list = []

while True:
    response = requests.get(full_url, params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancies = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    # print(url + vac_page['href'])
    for vac in vacancies:
        vac_data = {}
        vac_info = vac.find('a', attrs={'class': 'bloko-link'})
        vac_name = vac_info.text
        vac_data['title'] = vac_name
        vac_link = vac_info['href']
        vac_price_info = vac.find('div', attrs={'class', 'vacancy-serp-item__row_header'})
        vac_price = vac_price_info.find('div', attrs={'class', 'vacancy-serp-item__sidebar'})
        if vac_price is None:
            vac_data['salary'] = {
                'min_salary': 'not salary',
                'max_salary': 'not salary',
                'currency': 'not salary'
            }
        else:
            vac_price = vac_price.text
            if 'от' in vac_price:
                price = correct_price(vac_price, 'от ')
                vac_data['salary'] = {
                    'min_salary': price[0],
                    'max_salary': 'not salary',
                    'currency': price[1]
                }
            elif 'до' in vac_price:
                price = correct_price(vac_price, 'до ')
                vac_data['salary'] = {
                    'min_salary': 'not salary',
                    'max_salary': price[0],
                    'currency': price[1]
                }
            elif '–' in vac_price:
                price = correct_price(vac_price, '–')
                vac_data['salary'] = {
                    'min_salary': price[0],
                    'max_salary': price[1],
                    'currency': price[2]
                }

        vac_data['link'] = vac_link
        vac_data['site'] = url
        vacancies_list.append(vac_data)

    vac_page = soup.find('a', attrs={'data-qa': 'pager-next'})
    if vac_page:
        full_url = url + vac_page['href']
    else:
        break

df = pandas.DataFrame(vacancies_list)
df.to_csv('out.csv')
