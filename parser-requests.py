""" 
It is parser for moemisto.ua site.
It takes data from the site and put them to posgreSQL DB.
url format is [site]/[city]/[rubric]?days=[dd.mm.yyyy]
example: https://moemisto.ua/kiev/dityam?days=19.10.2021
where:
    site: https://moemisto.ua
    city is one of: kiev, vn, te, od, zt, km, lviv, kr
    rubric is one of: dityam, kontserti, dityam, podorozhi, vistavki, teatr, navchannya,
                    vidpochinok, suspilni-podiyi, sport, rozigrashi, shoping, kino,
                    vechirki, vidpochinok-v-inshomu-misti

Referense point for event name parsing:
<div class="thumbnail js-event-item"> caption
"""
import datetime
from datetime import timedelta
import requests
import re

from bs4 import BeautifulSoup
# config.py contains db paramenters for connection

from helper import clearDB, insertDB

def parser():
    now = datetime.datetime.now()
    site = 'https://moemisto.ua'
    cityes = {
        'kiev':'Київ',
        'vn':'Вінниця',
        'te':'Тернопіль',
        'od':'Одеса',
        'zt':'Житомир',
        'km':'Хмельницький',
        'lviv':'Львів',
        'kr':'Кропивницький'
    }
    rubrics = {
        'dityam':'Дітям',
        'kontserti':'Концерти',
        'podorozhi':'Подорожі',
        'vistavki':'Виставки',
        'teatr':'Театр',
        'navchannya':'Навчання',
        'vidpochinok':'Відпочинок',
        'suspilni-podiyi':'Суспільні події',
        'sport':'Спорт',
        'rozigrashi':'Розіграші',
        'shoping':'Шопінг',
        'kino':'Кіно',
        'vechirki':'Відпочинок',
        'vidpochinok-v-inshomu-misti':'В іншому місті'
        }

    """ # dataset for testing
    cityes = {
        'kiev':'Київ',
        'km':'Хмельницький'
    }
    rubrics = {
        'dityam':'Дітям',
        'kontserti':'Концерти'
        }
    """

    # clear database before inserting new parsed results
    clearDB()

    # interact site pages trow cityes, rubrics and dates
    for city in cityes.keys():
        print('Parsing city ' + cityes.get(city))
        for rubric in rubrics.keys():
            print('   rubric ' + rubrics.get(rubric))
            # from today + 31 day
            for i in range (0, 32):
                print('#', end = '')
                date = now + timedelta(days = i)
                day = str(date.day) + '.' + str(date.month) + '.' + str(date.year)
                url = site + '/' + city + '/' + rubric + '?days=' + day
                # read the site
                r = requests.get(url)
                text = r.text
                pattern = 'data-event-id="#(\d+)'
                eventIds = re.findall(pattern,text)
                # remove duplicates
                eventIds = list( dict.fromkeys(eventIds) )
                for eventId in eventIds:
                    # here we have city, rubric, date, eventId. Let's extract eventName with help of regular exspretions
                    pattern = 'data-event-id="#' + eventId + '">\s*(\s*.*)'
                    result = re.findall(pattern,text)
                    # event name is the last string in the results
                    for string in result:
                        eventName = string
                    # insert parsed data to database
                    insertDB(cityes.get(city), rubrics.get(rubric), date, eventId, eventName)
            print()
        
    print("Parsing finished in %s seconds" % (datetime.datetime.now() - now).total_seconds())


if __name__ == '__main__':
    parser()
