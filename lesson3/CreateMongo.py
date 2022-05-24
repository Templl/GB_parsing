from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

from pprint import pprint
import json
import re

#загружаем вакансии
with open('data.txt') as json_file:
    data = json.load(json_file)

#добавляем индетификатор вакансии
for vacancy in data:
    link = vacancy['link']
    id = re.split('/', link)[4]
    vacancy['_id'] = id[:8]


###
#подключаемся к базе монго
client = MongoClient('127.0.0.1', 27017)
db = client['vacncy2005']  # база данных
vacancy = db.vacancy  # название коллекции

#загружаем в базу вакансии
for i in range(len(data)):
    try:
        vacancy.insert_one(data[i])
    except dke:
        #print(f'Вакансия "{data[i]["name"]}" уже есть в базе')
