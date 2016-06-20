# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import os
import re
import requests
import time
import urllib2

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import *
from wechat_sdk.messages import *
from wechat_sdk.context.framework.django import DatabaseContextStore

from models import FilmSearch, Films, Notes, TempItemStorage, ItemStorage


conf = WechatConf(
    token='ggfilm',
    appid='wxd215ea1905032a90',
    appsecret='14a0dc6d2dc81db94f46f2755f0f4702',
    encrypt_mode='normal',
    encoding_aes_key='1ULPjA9GkTFNqhawzSITtRCE5DrIsk7ggVZCg2EIMUI',
)

menu = {
    'button':[
        {
            'type': 'view',
            'name': '搜索参数',
            'url': 'http://www.fotolei.cn/search'
        },
        {
            'name': 'F1冲洗机',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '入门视频教程',
                    'url': 'http://www.summychou.me'
                },
            ]
        },
        {
            'name': '胶片教程',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '胶片存放',
                    'url': 'http://www.summychou.me'
                },
            ]
        }
    ]
}

wechat = WechatBasic(conf=conf)


@csrf_exempt
def index(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest("Failed!")
        return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")

    try:
        wechat.create_menu(menu_data=menu)
    except OfficialAPIError:
        return HttpResponseBadRequest('Failed to Create Menu')

    try:
        wechat.parse_data(request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid Body Text')    

    if isinstance(wechat.message, EventMessage):
        xml = wechat.response_text(content='感谢您关注龟龟摄影微信公众号！回复【历史消息】，查看往期推送信息；') 
        return HttpResponse(xml, content_type='application/xml')
    if isinstance(wechat.message, TextMessage):
        content = wechat.message.content.strip()
        if content == '历史消息':
            access_token_response = urllib2.urlopen(
                'https://api.weixin.qq.com/cgi-bin/token?grant_type'
                '=client_credential&appid=wxd215ea1905032a90&secret=14a0dc6d2dc81db94f46f2755f0f4702').read()
            access_token = json.loads(access_token_response).get('access_token')
            post_url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s' % access_token
            post_data = json.dumps({'type': "news", 'offset': 0, 'count': 4})
            response = requests.post(post_url, data=post_data).json()
            item_count = int(response["item_count"])
            media_id_list = []
            for j in range(item_count):
                media_id = response["item"][j]["media_id"]
                media_id_list.append(media_id)

            news_item_list = []
            for media_id in media_id_list:
                post_url = 'https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s' % access_token   
                post_data = json.dumps({'media_id': media_id})
                response = requests.post(post_url, data=post_data).json()
                news_item_list.append((response["news_item"][0]["title"].encode("raw_unicode_escape"),
                                       response["news_item"][0]["thumb_url"].encode("raw_unicode_escape"),
                                       response["news_item"][0]["url"].encode("raw_unicode_escape")))
            
            articles = []
            for j in range(item_count):
                articles.append({'title': news_item_list[j][0],
                                 'picurl': news_item_list[j][1],
                                 'url': news_item_list[j][2]})
            xml = wechat.response_news(articles)
            return HttpResponse(xml, content_type='application/xml')


def update_database(request):
    return render(request, "update.html")


@cache_page(60 * 30)
def search_database_film(request):
    films = Films.objects.all().order_by("Film")

    display_35mm = []
    for film in films:
        if FilmSearch.objects.filter(Film=film.Film).exclude(a35mm="").exists():
            display_35mm.append(FilmSearch.objects.filter(Film=film.Film).exclude(a35mm="")[0].Film)
    display_35mm_counts = len(display_35mm)

    display_120 = []
    for film in films:
        if FilmSearch.objects.filter(Film=film.Film).exclude(a120="").exists():
            display_120.append(FilmSearch.objects.filter(Film=film.Film).exclude(a120="")[0].Film)
    display_120_counts = len(display_120)

    display_sheet = []
    for film in films:
        if FilmSearch.objects.filter(Film=film.Film).exclude(Sheet="").exists():
            display_sheet.append(FilmSearch.objects.filter(Film=film.Film).exclude(Sheet="")[0].Film)
    display_sheet_counts = len(display_sheet)

    return render(request, "search_film.html", {"display_35mm": display_35mm,
                                                "display_35mm_counts": display_35mm_counts,
                                                "display_120": display_120,
                                                "display_120_counts": display_120_counts,
                                                "display_sheet": display_sheet,
                                                "display_sheet_counts": display_sheet_counts})


def search_database_developer(request):
    source = request.GET.get("source")
    film = request.GET.get("film").replace('^', '+')
    films_search = None
    if source == "135":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a35mm="")
    elif source == "120":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a120="")
    elif source == "页片":
        films_search = FilmSearch.objects.filter(Film=film).exclude(Sheet="")
    display_developer = []
    for film_search in films_search:
        if film_search.Developer not in display_developer:
            display_developer.append(film_search.Developer)
    display_developer_counts = len(display_developer)
    return render(request, "search_developer.html", {"nav": {"source": source, "film": film},
                                                     "display_developer": display_developer,
                                                     "display_developer_counts": display_developer_counts})


def search_database_dilution(request):
    source = request.GET.get("source")
    film = request.GET.get("film").replace('^', '+')
    developer = request.GET.get("developer").replace('^', '+')
    films_search = None
    if source == "135":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a35mm="").filter(Developer=developer)
    elif source == "120":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a120="").filter(Developer=developer)
    elif source == "页片":
        films_search = FilmSearch.objects.filter(Film=film).exclude(Sheet="").filter(Developer=developer)
    display_dilution = []
    for film_search in films_search:
        if film_search.Dilution not in display_dilution:
            display_dilution.append(film_search.Dilution)
    display_dilution_counts = len(display_dilution)
    return render(request, "search_dilution.html", {"nav": {"source": source, "film": film, "developer": developer},
                                                    "display_dilution": display_dilution,
                                                    "display_dilution_counts": display_dilution_counts})


def search_database_asa_iso(request):
    source = request.GET.get("source")
    film = request.GET.get("film").replace('^', '+')
    developer = request.GET.get("developer").replace('^', '+')
    dilution = request.GET.get("dilution").replace('^', '+')
    films_search = None
    if source == "135":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a35mm="").filter(Developer=developer).filter(Dilution=dilution)
    elif source == "120":
        films_search = FilmSearch.objects.filter(Film=film).exclude(a120="").filter(Developer=developer).filter(Dilution=dilution)
    elif source == "页片":
        films_search = FilmSearch.objects.filter(Film=film).exclude(Sheet="").filter(Developer=developer).filter(Dilution=dilution)
    display_asa_iso = []
    for film_search in films_search:
        if film_search.ASA_ISO not in display_asa_iso:
            display_asa_iso.append(film_search.ASA_ISO)
    display_asa_iso_counts = len(display_asa_iso)
    return render(request, "search_asa_iso.html", {"nav": {"source": source, "film": film, "developer": developer,
                                                           "dilution": dilution},
                                                   "display_asa_iso": display_asa_iso,
                                                   "display_asa_iso_counts": display_asa_iso_counts})


def search_database_result(request):
    source = request.GET.get("source")
    film = request.GET.get("film").replace('^', '+')
    developer = request.GET.get("developer").replace('^', '+')
    dilution = request.GET.get("dilution").replace('^', '+')
    asa_iso = request.GET.get("asa_iso").replace('^', '+')
    result = None
    if source == "135":
        result = FilmSearch.objects.filter(Film=film).exclude(a35mm="").filter(Developer=developer).filter(Dilution=dilution).filter(ASA_ISO=asa_iso)[0]
    elif source == "120":
        result = FilmSearch.objects.filter(Film=film).exclude(a120="").filter(Developer=developer).filter(Dilution=dilution).filter(ASA_ISO=asa_iso)[0]
    elif source == "页片":
        result = FilmSearch.objects.filter(Film=film).exclude(Sheet="").filter(Developer=developer).filter(Dilution=dilution).filter(ASA_ISO=asa_iso)[0]

    time = ""
    if source == "135":
        time = result.a35mm
    elif source == "120":
        time = result.a120
    elif source == "页片":
        time = result.Sheet

    temperature = result.Temp.split("C")[0]

    note_list = []
    if result.Notes != "":
        note_orders = result.Notes
        note_orders = re.findall(r"\[(.*?)\]", note_orders)
        for note_order in note_orders:
            if note_order == "46":
                pass
            else:
                note = Notes.objects.get(Notes=note_order).Remark
                note_list.append(note)
    has_note = len(note_list)
    return render(request, "search_result.html", {"nav": {"source": source, "film": film, "developer": developer,
                                                          "dilution": dilution, "asa_iso": asa_iso},
                                                  "time": time,
                                                  "temperature": temperature,
                                                  "has_note": has_note,
                                                  "note_list": note_list})


phone_list = ["15527011768", ]


def buyer_authenticate(request):
    if request.is_ajax() and request.method == "POST":
        if request.POST.get("type") == "1":
            phone = request.POST.get("inputPhone").strip()
            if phone in phone_list:
                json_data = json.dumps({"msg": "号码验证成功！", "flag": "true"})
                return HttpResponse(json_data)
            else:
                json_data = json.dumps({"msg": "号码验证失败！抱歉，您不是我们的客户！", "flag": "false"})
                return HttpResponse(json_data)
        elif request.POST.get("type") == "2":
            subject = "龟龟摄影微信公众号"
            text_content = "这是一封来自龟龟摄影微信公众号的邮件！" \
                           "附件中携带了您需要的资料。"
            html_content = "<p>这是一封来自<strong>龟龟摄影微信公众号</strong>的邮件！</p>" \
                           "<p><strong>附件</strong>中携带了您需要的资料。</p>"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = request.POST.get("inputEmail").strip()
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.attach_file("media/resources/hacker.jpg")
            msg.send()
            return HttpResponse("邮件发送成功！")
    return render(request, "buyer_authenticate.html")


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


def remove_pics(fp):
    root_dir = 'media/pic'
    for root, dirs, files in os.walk(root_dir):
        print >> fp, u'正在删除图片...'.encode('utf-8')
        for filename in files:
            os.remove(root+'/'+filename)
        print >> fp, u'图片删除完毕'.encode('utf-8')


def find_out_real_price(shop_url, match_price):
    html = urllib2.urlopen(shop_url).read()
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    title = soup.find(name='h3', attrs={'class': 'tb-main-title'})['data-title'].strip()
    price = soup.find(name='li', attrs={'id': 'J_StrPriceModBox'}). \
        find(name='em', attrs={'class': 'tb-rmb-num'}).get_text().strip()
    if match_price != price:
        taobao_price = match_price
    else:
        taobao_price = ''
    return title, price, taobao_price


def price_trace(request):
    if request.is_ajax() and request.method == "GET":
        if request.GET.get("type") == "1":
            # 清空数据表中已存在的记录
            TempItemStorage.objects.all().delete()

            keywords = request.GET.get("inputKeywords").strip()

            f = open('logs/price_trace.log', 'a')
            print >> f, '******************************'
            print >> f, '     ' + get_current_time()
            print >> f, '******************************'
            remove_pics(f)

            url = 'https://www.taobao.com/'
            try:
                new_driver = webdriver.PhantomJS('/usr/lib/phantomjs/phantomjs')
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

                        # 发送搜索词
                        search_input.send_keys(keywords)

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

                            # 抓取商品图
                            for (j, item) in enumerate(all_items):
                                print >> f, u'正在爬取第{0}家店铺的数据...'.format(j + 1).encode('utf-8')
                                item_pic = WebDriverWait(item, 10).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, 'J_ItemPic'))
                                )
                                item_pic_src = item_pic.get_attribute('src')
                                item_pic_id = item_pic.get_attribute('id')
                                try:
                                    im = Image.open(StringIO(requests.get(item_pic_src, timeout=5).content))
                                    if im.mode != 'RGB':
                                        im = im.convert('RGB')
                                    try:
                                        im.save('media/pic/{0}.webp'.format(item_pic_id))
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
                                # 存储数据
                                obj = TempItemStorage(ItemLink=item_link, ItemPicId=item_pic_id,
                                                      ItemTitle=item_title, ItemShopName=item_shop_name,
                                                      ItemLocation=item_location, ItemPrice=item_price,
                                                      ItemTaoBaoPrice=item_taobao_price, ItemDeal=item_deal)
                                obj.save()
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
            return HttpResponse()
    if request.is_ajax() and request.method == "POST":
        if request.POST.get("type") == "2":
            add_item_link = request.POST.get("item_link")
            add_item_title = request.POST.get("item_title")
            add_item_shopname = request.POST.get("item_shopname")
            add_item_price = request.POST.get("item_price")
            add_item_taobao_price = request.POST.get("item_taobao_price")

            temp_item = TempItemStorage.objects.filter(ItemTitle=add_item_title)\
                .filter(ItemShopName=add_item_shopname) \
                .filter(ItemPrice=add_item_price)[0]
            temp_item.Has_Been_Selected = True
            temp_item.save()

            item = ItemStorage(ItemLink=add_item_link, ItemTitle=add_item_title,
                               ItemShopName=add_item_shopname, ItemPrice=add_item_price,
                               ItemTaoBaoPrice=add_item_taobao_price)
            item.save()
            return HttpResponse()
    cached_item_list = TempItemStorage.objects.all()
    return render(request, "price_trace.html", {"item_list": cached_item_list})
