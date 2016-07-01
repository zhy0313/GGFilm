# !/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

from django.http import HttpResponse

from models import FilmSearch

headers = {"UserAgent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36"}


def update_database(request):
    if request.is_ajax():
        url = "http://www.digitaltruth.com/chart/print.php"
        response = urllib2.Request(url, headers=headers)
        html = urllib2.urlopen(response).read()
        soup = BeautifulSoup(html, 'lxml', from_encoding='utf8')
        tr = soup.find_all(name='tr')[1]

        for td in tr.find_all(name='td')[2:5]:
            for a in td.find_all(name='a'):
                url_link = 'http://www.digitaltruth.com/' + a['href']
                response = urllib2.Request(url_link, headers=headers)
                html = urllib2.urlopen(response).read()
                soup = BeautifulSoup(html, 'lxml', from_encoding='utf8')
                for tr in soup.find_all('tr')[1:]:
                    film = tr.find_all('td')[0].get_text()
                    developer = tr.find_all('td')[1].get_text()
                    dilution = tr.find_all('td')[2].get_text()
                    asa_iso = tr.find_all('td')[3].get_text()
                    a35mm = tr.find_all('td')[4].get_text()
                    a120 = tr.find_all('td')[5].get_text()
                    sheet = tr.find_all('td')[6].get_text()
                    temp = tr.find_all('td')[7].get_text()
                    notes = tr.find_all('td')[8].get_text()
                    try:
                        film_search = FilmSearch.objects.get(Film=film, Developer=developer,
                                                             Dilution=dilution, ASA_ISO=asa_iso)
                    except FilmSearch.DoesNotExist:
                        film_search = FilmSearch(
                            Film=film, Developer=developer, Dilution=dilution,
                            ASA_ISO=asa_iso, a35mm=a35mm, a120=a120,
                            Sheet=sheet, Temp=temp, Notes=notes
                        )
                        film_search.save()
        return HttpResponse(u"更新数据库完毕！")
