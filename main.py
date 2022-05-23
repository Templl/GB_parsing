#import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
#import pprint
import re

main_url = 'https://hh.ru'
vacancy = 'Data Scientist'
page = 0
all_vacancies = []
params = {'text': vacancy,
          'area': 1,
          'experience': 'doesNotMatter',
          'order_by': 'relevance',
          'search_period': 0,
          'items_on_page': 20,
          'page': page}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         'Chrome/98.0.4758.141 YaBrowser/22.3.4.731 Yowser/2.5 Safari/537.36'}

response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)

with open('page.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

html = ''
with open('page.html', encoding='utf-8', mode='r') as f:
    html = f.read()

soup = bs(html, 'html.parser')
body = soup.find('body')

vacancy1 = body.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})

for vac in vacancy1:
    vacancy_info = {}
    min_sal = 0
    # название вакансии
    vac_a = vac.find('a', {'data-qa': "vacancy-serp__vacancy-title"})
    name = vac_a.getText()
    vacancy_info['name'] = name

    # ссылка
    vacancy_link = vac_a['href']
    vacancy_info['link'] = vacancy_link
    # print(vacancy_link)

    # з/п
    vac_salary = vac.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})
    if vac_salary == None:
        min_salary = None
        max_salary = None
        currency = None

    if vac_salary != None:
        vacancy_salary = vac_salary.getText()
        # print(vacancy_salary)
        if vacancy_salary.startswith('до'):
            string = re.split(' ', vacancy_salary)[1]
            num = ''
            for s in string:
                if s.isdigit():
                    num += s
            max_salary = int(num)
            min_salary = None
            currency = re.split(' ', vacancy_salary)[2]
            print(currency)
        elif vacancy_salary.startswith('от'):
            max_salary = None
            string = re.split(' ', vacancy_salary)[1]
            num = ''
            for s in string:
                if s.isdigit():
                    num += s
            min_salary = int(num)
            currency = re.split(' ', vacancy_salary)[2]
        else:
            string = re.split(' ', vacancy_salary)[0]
            num = ''
            for s in string:
                if s.isdigit():
                    num += s
            min_salary = int(num)
            string = re.split(' ', vacancy_salary)[2]
            num = ''
            for s in string:
                if s.isdigit():
                    num += s
            max_salary = int(num)
            currency = re.split(' ', vacancy_salary)[3]

    vacancy_info['макс'] = max_salary
    vacancy_info['мин']  = min_salary
    vacancy_info['валюта'] = currency

    print(vacancy_info)


