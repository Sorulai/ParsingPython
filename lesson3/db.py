# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).


from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
hh = db.hh
usd = 72.77
eur = 84.38

user_message = int(input('Введите минимальную сумму заработной платы,которая вас устраивает: '))


def find_vacancies(database, message, USD=usd, EUR=eur):
    print(f'Вакансии, зарплата которых начинает от {message} руб')
    for doc in database.find({'$or': [{'salary.min_salary': {'$gte': message},
                                       'salary.currency': 'руб.'
                                       }, {
                                          'salary.min_salary': {'$gte': message / USD},
                                          'salary.currency': 'USD'

                                      }, {
                                          'salary.min_salary': {'$gte': message / EUR},
                                          'salary.currency': 'EUR'

                                      }

                                      ]
                              }):
        print(
            f'{doc["title"]} , зарплата от {doc["salary"]["min_salary"]} {doc["salary"]["currency"]}, ссылка на вакансию {doc["link"]}')

    print('----------------------------------------------')
    print(f'Вакансии, зарплата которых может быть больше {message} руб, но она не стартовая')
    for doc in database.find({'$or': [{'salary.max_salary': {'$gte': message},
                                       'salary.currency': 'руб.'
                                       }, {
                                          'salary.max_salary': {'$gte': message / USD},
                                          'salary.currency': 'USD'

                                      }, {
                                          'salary.max_salary': {'$gte': message / EUR},
                                          'salary.currency': 'EUR'

                                      }

                                      ]
                              }):
        print(
            f'{doc["title"]} , зарплата до {doc["salary"]["max_salary"]} {doc["salary"]["currency"]}, ссылка на вакансию {doc["link"]}')


find_vacancies(hh, user_message)
