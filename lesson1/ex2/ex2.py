# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

api_key = ''
breed = 'ragd'
my_params = {
    'breed_id': breed,
    'api_key': api_key
}
url_img_breed = f'https://api.thecatapi.com/v1/images/search'

response = requests.get(url_img_breed, params=my_params)
with open('ex2.json', mode='w', encoding='utf8') as file:
    json.dump(response.json(), file)
