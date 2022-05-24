from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

from pprint import pprint

#current_course =

#подключаемся к базе монго
client = MongoClient('127.0.0.1', 27017)
db = client['vacncy2005']  # база данных
vacancy = db.vacancy  # название коллекции

# вводе переменных для поиска
salary = input('Желаемая зарплата:')
currency = input('В какой валюте зарплата:')

#salary = 220000
#currency = 'руб.'

#result = list(vacancy.find({}))
#pprint(result)

for doc in vacancy.find(
        {'мин': {'$gte': salary},
         'макс': {'$gte': salary},
         'валюта': {'$eq': currency}}
):
    if doc == None:
        print('вакансии с такими параметрами не найдены')
    else:
        pprint(doc)

result = list(vacancy.find(
                            {'мин': {'$gte': salary},
                             'макс': {'$gte': salary},
                             'валюта': {'$eq': currency}}
))

if len(result):
    pprint(result)
else:
    print('Подходящих вакансий не найдено')