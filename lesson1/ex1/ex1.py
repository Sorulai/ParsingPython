# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

token = ''
user = 'Sorulai'
url = 'https://api.github.com/user'

response = requests.get(url, auth=(user, token))
url_repo = response.json().get('repos_url')

response_repo = requests.get(url_repo, auth=(user, token))
j_data_repo = response_repo.json()

filename = 'ex1.json'
with open(filename, mode='w', encoding='utf8') as file:
    json.dump(j_data_repo, file)

for el in j_data_repo:
    with open('titles_repo.txt', mode='a', encoding='utf8') as file:
        file.write(f'{el.get("full_name")} + \n')
