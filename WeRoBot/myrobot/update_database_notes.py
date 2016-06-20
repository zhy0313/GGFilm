# !/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup

from django.http import HttpResponse

from models import Notes

headers = {"UserAgent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36"}


def update_database(request):
    if request.is_ajax():
        url = "http://www.digitaltruth.com/chart/notes.php"
        response = urllib2.Request(url, headers=headers)
        html = urllib2.urlopen(response).read()
        soup = BeautifulSoup(html, 'lxml', from_encoding='utf8')
        for tr in soup.find_all(name='tr'):
            extract_list = tr.find_all(name='td')
            if (extract_list[0].get_text() == '42' or extract_list[0].get_text() == '43' or
                    extract_list[0].get_text() == '44' or extract_list[0].get_text() == '45'):
                content = extract_list[1].get_text().split('see')[0].strip()
                note = Notes(Notes=extract_list[0].get_text(), Remark=content)
                note.save()
            elif extract_list[0].get_text() == '46':
                pass
            else:
                note = Notes(Notes=extract_list[0].get_text(), Remark=extract_list[1].get_text())
                note.save()
        return HttpResponse(u"更新数据库完毕！")
