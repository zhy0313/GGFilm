# -*- coding: utf-8 -*-
import os
import re
import time
import urllib2

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeRoBot.settings")


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def parse_update_data(html, f_log):
    print >> f_log, u"进入数据更新页面...".encode('utf-8')
    soup_outer = BeautifulSoup(html, "lxml", from_encoding="utf-8")
    for tr in soup_outer.find_all(name="tr")[1:]:
        td = tr.find_all(name="td")
        film = td[0].get_text().strip()
        developer = td[1].get_text().strip()
        dilution = td[2].get_text().strip()
        asa_iso = td[3].get_text().strip()
        a35mm = td[4].get_text().strip()
        a120 = td[5].get_text().strip()
        sheet = td[6].get_text().strip()
        temp = td[7].get_text().strip()
        try:
            notes_link = td[8].find(name="a").get("href")
            notes_link = "http://www.digitaltruth.com/"+notes_link
            notes_html = urllib2.urlopen(notes_link).read()
            soup_inner = BeautifulSoup(notes_html, "lxml", from_encoding="utf8")
            notes = soup_inner.find_all(name="tr")[1].find_all(name="td")[-1].get_text().strip()
        except AttributeError, error:
            notes = ""
        from myrobot.models import FilmSearch
        try:
            obj = FilmSearch.objects.get(Film=film, Developer=developer, Dilution=dilution,
                                         ASA_ISO=asa_iso, Temp=temp)
            obj.a35mm = a35mm
            obj.a120 = a120
            obj.sheet = sheet
            obj.Notes = notes
            obj.save()
            print >> f_log, u'更新FilmSearch数据项'.encode('utf-8')
        except FilmSearch.DoesNotExist:
            obj = FilmSearch(Film=film, Developer=developer, Dilution=dilution, ASA_ISO=asa_iso,
                             a35mm=a35mm, a120=a120, Sheet=sheet, Temp=temp, Notes=notes)
            obj.save()
            print >> f_log, u'新增FilmSearch数据项'.encode('utf-8')
        from myrobot.models import Films
        try:
            obj = Films.objects.get(Film=film)
        except Films.DoesNotExist:
            obj = Films(Film=film)
            obj.save()
            print >> f_log, u'新增Films数据项'.encode('utf-8')


if __name__ == '__main__':
    f = open('logs/data_update.log', 'a')
    print >> f, '******************************'
    print >> f, '     '+get_current_time()
    print >> f, '******************************'

    tracked_url = "http://www.digitaltruth.com/devchart.php?doc=search"

    tracked_html = urllib2.urlopen(tracked_url).read()
    soup = BeautifulSoup(tracked_html, "lxml", from_encoding="utf8")
    last_update = soup.find_all(name="form")[1].find(name="p").get_text()
    last_update_datetime = re.findall(r":(.*?)\[", last_update, re.S)[0].strip()
    with open("last_update_datetime.txt", "w+") as fp:
        stored_datetime = fp.read().strip()
        if last_update_datetime != stored_datetime:
            fp.write(last_update_datetime)
            try:
                driver = webdriver.PhantomJS()
                driver.set_window_size(800, 400)
                try:
                    driver.get("http://www.digitaltruth.com/devchart.php?doc=search")
                    try:
                        latest_changes_link_wrap = WebDriverWait(driver, 10).until(
                            expected_conditions.presence_of_element_located((By.XPATH, "//form[@name='idForm']"))
                        )
                        latest_changes_link = WebDriverWait(latest_changes_link_wrap, 10).until(
                            expected_conditions.presence_of_element_located((By.TAG_NAME, "a"))
                        )
                        latest_changes_link.click()
                        time.sleep(5)
                        parse_update_data(driver.page_source, f)
                        driver.close()
                    except NoSuchElementException, e:
                        driver.close()
                        print >> f, e
                except TimeoutException, e:
                    driver.close()
                    print >> f, e
            except WebDriverException, e:
                print >> f, e
    f.close()
