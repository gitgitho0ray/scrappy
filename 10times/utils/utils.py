from bs4 import BeautifulSoup
import requests
import re
from time import strptime
import datetime
from datetime import datetime
from calendar import monthrange
from datetime import timedelta
import pandas as pd

class EventDate():

    def __init__(self, eventdate):

        if len(eventdate) == 4:
            sday = int(strptime(eventdate[0], '%d').tm_mday)
            month = int(strptime(eventdate[2], '%b').tm_mon)
            eday = int(strptime(eventdate[1], '%d').tm_mday)
            year = int(strptime(eventdate[-1], '%Y').tm_year)
            self.startdate = datetime.date(datetime(year, month, sday))
            self.enddate = datetime.date(datetime(year, month, eday))

        elif len(eventdate) == 5:
            sday = int(strptime(eventdate[0], '%d').tm_mday)
            smonth = int(strptime(eventdate[1], '%b').tm_mon)
            eday = int(strptime(eventdate[2], '%d').tm_mday)
            emonth = int(strptime(eventdate[3], '%b').tm_mon)
            year = int(strptime(eventdate[-1], '%Y').tm_year)
            self.startdate = datetime.date(datetime(year, smonth, sday))
            self.enddate = datetime.date(datetime(year, emonth, eday))

        else:
            sday = int(strptime(eventdate[0], '%d').tm_mday)
            month = int(strptime(eventdate[1], '%b').tm_mon)
            eday = int(strptime(eventdate[0], '%d').tm_mday)
            year = int(strptime(eventdate[-1], '%Y').tm_year)
            self.startdate = datetime.date(datetime(year, month, sday))
            self.enddate = datetime.date(datetime(year, month, eday))


class SearchDate():

    def __init__(self, today='', endofweek='', endofthemonth=''):
        self.today = str(datetime.now().date())
        self.addoneweek = str((datetime.now().date() + timedelta(days=7)))
        self.endofthemonth = str(datetime(datetime.now().year, datetime.now().month,
                                          monthrange(datetime.now().year, datetime.now().month)[1]).date())


class ScrappyDoo():
    def __init__(self, url=''):
        self.url = url

    def get_content(self):

        def get_html(url, params=None):
            h = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel) Gecko/20100101 Firefox/74.0'}
            response = requests.get(self.url, params=params, headers=None)
            return response.text

        soup = BeautifulSoup(get_html(self.url), 'html.parser')
        items = soup.find_all('tr', class_='box')
        events = [i.find('a', {'target': '_blank'}).get('href') for i in items if
                  i.find('a', {'target': '_blank'}) != None]
        return events

    def parse():
        html = get_html(url)
        if html.status_code == 200:
            get_content(html.text)
        else:
            print('error')
        return html
