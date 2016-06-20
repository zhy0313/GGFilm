#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
import requests
import time
import urllib2

from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def remove_pics(fp):
    root_dir = '/home/summy/WeChatApplication/WeRoBot/media/pic'
    for root, dirs, files in os.walk(root_dir):
        print >> fp, u'正在删除图片...'.encode('utf-8')
        for filename in files:
            os.remove(root+'/'+filename)
        print >> fp, u'图片删除完毕'.encode('utf-8')


def find_out_real_price(shop_url, match_price):
    html = urllib2.urlopen(shop_url).read()
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    title = soup.find(name='h3', attrs={'class': 'tb-main-title'})['data-title'].strip()
    price = soup.find(name='li', attrs={'id': 'J_StrPriceModBox'}).\
        find(name='em', attrs={'class': 'tb-rmb-num'}).get_text().strip()
    if match_price != price:
        taobao_price = match_price
    else:
        taobao_price = 'None'
    return title, price, taobao_price


if __name__ == '__main__':
    f = open('logs/price_trace.log', 'a')
    print >> f, '******************************'
    print >> f, '     '+get_current_time()
    print >> f, '******************************'
    remove_pics(f)

    url = 'https://www.taobao.com/'
    try:
        new_driver = webdriver.PhantomJS()
        new_driver.set_window_size(1366, 768)
        try:
            print >> f, u'模拟登录淘宝网'.encode('utf-8')
            new_driver.get(url)
            try:
                search_combobox = WebDriverWait(new_driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'search-combobox-input-wrap'))
                )
                search_input = WebDriverWait(search_combobox, 10).until(
                    EC.presence_of_element_located((By.ID, 'q'))
                )

                # input_keywords = raw_input()
                input_keywords = u'依尔福DDX ILFORD DD-X 伊尔福 超微粒 通用黑白胶卷冲洗'
                # search_input.send_keys(input_keywords.decode('utf-8'))
                search_input.send_keys(input_keywords)

                search_button_wrap = WebDriverWait(new_driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'search-button'))
                )
                search_button = WebDriverWait(search_button_wrap, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'btn-search'))
                )
                search_button.click()
                try:
                    print >> f, u'搜索成功，正在返回搜索结果...'.encode('utf-8')
                    main_srp_item_list = WebDriverWait(new_driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'mainsrp-itemlist'))
                    )
                    m_item_list = WebDriverWait(main_srp_item_list, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'm-itemlist'))
                    )
                    items = WebDriverWait(m_item_list, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'items'))
                    )[0]
                    all_items = WebDriverWait(items, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'item'))
                    )
                    total_items = len(all_items)
                    print >> f, u'总共返回{0}个搜索结果'.format(total_items).encode('utf-8')
                    cached_item_list = []
                    # 抓取商品图
                    for (j, item) in enumerate(all_items):
                        print >> f, u'正在爬取第{0}家店铺的数据...'.format(j+1).encode('utf-8')
                        item_pic = WebDriverWait(item, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'J_ItemPic'))
                        )
                        item_pic_src = item_pic.get_attribute('src')
                        try:
                            im = Image.open(StringIO(requests.get(item_pic_src, timeout=5).content))
                            if im.mode != 'RGB':
                                im = im.convert('RGB')
                            try:
                                im.save('media/pic/{0}.webp'.format(j+1))
                            except IOError, e:
                                print >> f, e
                        except requests.Timeout, e:
                            print >> f, e
                        item_price_and_link = WebDriverWait(item, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'J_ClickStat'))
                        )
                        item_match_price = item_price_and_link.get_attribute('trace-price')
                        item_link = item_price_and_link.get_attribute('href')
                        item_title, item_price, item_taobao_price = find_out_real_price(item_link, item_match_price)

                        item_deal = WebDriverWait(item, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'deal-cnt'))
                        ).text

                        row_3 = WebDriverWait(item, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'row-3'))
                        )
                        item_shop_name = WebDriverWait(row_3, 10).until(
                            EC.presence_of_all_elements_located((By.TAG_NAME, 'span'))
                        )[4].text

                        item_location = WebDriverWait(item, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'location'))
                        ).text
                    print >> f, u'数据爬取完毕'.encode('utf-8')
                    f.close()
                    new_driver.close()
                except NoSuchElementException, e:
                    new_driver.close()
                    print >> f, e
            except NoSuchElementException, e:
                new_driver.close()
                print >> f, e
        except TimeoutException, e:
            new_driver.close()
            print >> f, e
    except WebDriverException, e:
        print >> f, e
