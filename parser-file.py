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
import time
import threading
from datetime import timedelta
import requests
import re
from bs4 import BeautifulSoup
from helper import clearDB, fileToDB
import os

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

# lock needed for blocking shared resourses by active thread
lock = threading.Lock()

def processUrl(url, date):
    # read the site
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("================ Connection refused! url = " + url)
    
    # parse data from the site extract event IDs
    text = r.text
    pattern = 'data-event-id="#(\d+)'
    eventIds = re.findall(pattern,text)
    # remove duplicates
    eventIds = list( dict.fromkeys(eventIds) )

    # extract eventName
    for eventId in eventIds:
        pattern = 'data-event-id="#' + eventId + '">\s*(\s*.*)'
        result = re.findall(pattern,text)
        # event name is the last string in the results
        for string in result:
            eventName = string
        
        # block resourses (files for writing) for using by this thread only
        lock.acquire()
        try:
            # update temporary files with city, rubric, date, eventId and eventName
            fEvents.write("%s\t%s\n" %(eventId, eventName))
            fDates.write("%s\t%s\t%s\n" %(eventId, cityes.get(city), date))
            fRubrics.write("%s\t%s\n" %(eventId, rubrics.get(rubric)))
        finally:
            # release resourses
            lock.release()

def removeDuplicates(fName):
    f = open(fName, encoding=None)
    dataList = f.readlines()
    dataList = list(dict.fromkeys(dataList))
    f.close()

    f = open(fName, "w")
    f.writelines(dataList)
    f.close()

if __name__ == '__main__':
    now = datetime.datetime.now()
    clearDB()
    # prepare temporary files
    if os.path.exists("events.tsv"): os.remove("events.tsv")
    if os.path.exists("dates.tsv"): os.remove("dates.tsv")
    if os.path.exists("rubrics.tsv"): os.remove("rubrics.tsv")
    fEvents = open("events.tsv", "a")
    fDates = open("dates.tsv", "a")
    fRubrics = open("rubrics.tsv", "a")

    # interact site pages through cityes, rubrics and dates
    for city in cityes.keys():
        print('Start parsing city ' + cityes.get(city))
        for rubric in rubrics.keys():
            print('   rubric ' + rubrics.get(rubric) + '. Active threads: ' + str(threading.active_count()))
            # from today + 31 day
            for i in range (0, 31):
                date = now + timedelta(days = i)
                day = str(date.day) + '.' + str(date.month) + '.' + str(date.year)
                url = site + '/' + city + '/' + rubric + '?days=' + day

                # multithreading
                th = threading.Thread(target=processUrl, args=(url, date, ))
                th.start()
        print()

    # wait till all treads finished
    while threading.active_count() > 1:
        time.sleep(1)
    print("All threads finished")

    # close temporary files
    fEvents.close()
    fDates.close()
    fRubrics.close()

    # remove duplicates in temporary files
    removeDuplicates('events.tsv')
    removeDuplicates('dates.tsv')
    removeDuplicates('rubrics.tsv')

    #copy from files to DB
    fileToDB('events.tsv', 'events')
    fileToDB('dates.tsv', 'dates')
    fileToDB('rubrics.tsv', 'rubrics')

    print("Whole process finished in %s seconds" % (datetime.datetime.now() - now).total_seconds())