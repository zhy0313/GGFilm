# -*- coding: utf-8 -*-
import os
import time
import urllib2

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeRoBot.settings')


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def parse_price_sim(url, fff, new_driver):
    # try:
    #     new_driver.get(url)
        # try:
        #     username_input_field = WebDriverWait(new_driver, 10).until(
        #         expected_conditions.presence_of_element_located((By.CLASS_NAME, 'username-field'))
        #     )
        #     username_input_box = WebDriverWait(username_input_field, 10).until(
        #         expected_conditions.presence_of_element_located((By.TAG_NAME, 'input'))
        #     )
        #     username_input_box.send_keys("")
        #     password_input_field = WebDriverWait(new_driver, 10).until(
        #         expected_conditions.presence_of_element_located((By.CLASS_NAME, 'pwd-field'))
        #     )
        #     password_input_box = WebDriverWait(password_input_field, 10).until(
        #         expected_conditions.presence_of_element_located((By.TAG_NAME, 'input'))
        #     )
        #     password_input_box.send_keys("")
        #     login_button = WebDriverWait(new_driver, 10).until(
        #         expected_conditions.presence_of_element_located((By.ID, 'J_SubmitStatic'))
        #     )
        #     login_button.click()
        #
        #     search_result = WebDriverWait(new_driver, 10).until(
        #         expected_conditions.presence_of_element_located((By.CLASS_NAME, 'search-result'))
        #     )
        #     search_result_box = WebDriverWait(search_result, 10).until(
        #         expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'search-result-box'))
        #     )[0]
        #     title = WebDriverWait(search_result_box, 10).until(
        #         expected_conditions.presence_of_element_located((By.CLASS_NAME, 'title'))
        #     )
        #     link = WebDriverWait(title, 10).until(
        #         expected_conditions.presence_of_element_located((By.TAG_NAME, 'a'))
        #     ).get_attribute('href')

            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

            try:
                price = soup.find(name='li', attrs={'id': 'J_StrPriceModBox'}).\
                    find(name='em', attrs={'class': 'tb-rmb-num'}).get_text().strip()
            except Exception, e:
                temp_driver = webdriver.PhantomJS()
                temp_driver.set_window_size(800, 400)
                temp_driver.get(url)
                tm_fcs_panel = WebDriverWait(temp_driver, 10).until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, 'tm-fcs-panel'))
                )
                # price = WebDriverWait(tm_fcs_panel, 10).until(
                #     expected_conditions.presence_of_element_located((By.TAG_NAME, 'span'))
                # ).text
                price = WebDriverWait(tm_fcs_panel, 10).until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, 'tm-price'))
                ).text
                temp_driver.close()
            # TODO
            taobao_price = ''
            return price, taobao_price
    #     except NoSuchElementException, e:
    #         print >> fff, e
    #         new_driver.close()
    # except TimeoutException, e:
    #     print >> fff, e
    #     new_driver.close()


def parse_price(url, ff, new_driver):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    try:
        price = soup.find(name='li', attrs={'id': 'J_StrPriceModBox'}).\
            find(name='em', attrs={'class': 'tb-rmb-num'}).get_text().strip()
        taobao_price = ''
        print "{0} / {1}".format(price, taobao_price)
    except AttributeError, e:
        # TODO
        price, taobao_price = parse_price_sim(url, ff, new_driver)
        print "{0} / {1}".format(price, taobao_price)
    return price, taobao_price


def main():
    current_time = get_current_time()
    f = open('logs/price_data_update.log', 'a')
    print >> f, '******************************'
    print >> f, '     ' + current_time
    print >> f, '******************************'

    changed_list = []

    try:
        driver = webdriver.PhantomJS()
        driver.set_window_size(800, 400)
    except WebDriverException, error:
        print >> f, error

    from myrobot.models import ItemStorage
    all_items = ItemStorage.objects.all().order_by("id")
    for (j, item) in enumerate(all_items):
        print >> f, u"开始跟踪第{0}件商品的数据".encode('utf-8').format(j + 1)
        item_price, item_taobao_price = parse_price(item.ItemLink, f, driver)
        if item_price != item.ItemPrice or item_taobao_price != item.ItemTaoBaoPrice:
            if item_price != item.ItemPrice:
                print >> f, u"商品发生价格(市场价格)改动".encode('utf-8')
                # price_diff = float(item_price) - float(item.ItemPrice)
                item.ItemPrice = item_price
            else:
                print >> f, u"商品发生价格(淘宝价格)改动".encode('utf-8')
                # taobao_price_diff = float(item_taobao_price) - float(item.ItemPrice)
                item.ItemTaoBaoPrice = item_taobao_price
            item.save()
            changed_list.append(item)
        else:
            print >> f, u"商品没有发生价格改动".encode('utf-8')
        print >> f, u"第{0}件商品的数据跟踪结束".encode('utf-8').format(j + 1)
    driver.close()

    if len(changed_list) != 0:
        from django.conf import settings
        from django.core.mail import EmailMultiAlternatives
        subject = "龟龟摄影微信服务器"
        text_content = "这是一封来自龟龟摄影微信服务器的邮件！" \
                       "附件中携带了竞争对手的商品价格变动信息，" \
                       "总共有{0}家竞争对手的商品价格发生了变动。".format(len(changed_list))
        html_content = "<p>这是一封来自<strong>龟龟摄影微信服务器</strong>的邮件！</p>" \
                       "<p><strong>附件</strong>中携带了竞争对手的商品价格变动信息，" \
                       "总共有{0}家竞争对手的商品价格发生了变动。</p>".format(len(changed_list))
        from_email = settings.DEFAULT_FROM_EMAIL
        # to_email = "zhoujian@hust.edu.cn"
        to_email = "dinglin@mazhou.net"  # 你的邮箱地址
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")

        import xlwt
        excel = xlwt.Workbook()
        sheet = excel.add_sheet('DataSheet', cell_overwrite_ok=True)
        sheet.write(0, 0, u"商品名称")
        sheet.write(0, 1, u"店铺名称")
        sheet.write(0, 2, u"商品描述")
        sheet.write(0, 3, u"商品价格")
        sheet.write(0, 4, u"商品淘宝价格")
        sheet.write(0, 5, u"更新时间")
        sheet.write(0, 6, u"店铺淘宝地址")
        for (j, item) in enumerate(changed_list):
            sheet.write(j + 1, 0, item.ItemProductName)
            sheet.write(j + 1, 1, item.ItemShopName)
            sheet.write(j + 1, 2, item.ItemTitle)
            sheet.write(j + 1, 3, item.ItemPrice)
            sheet.write(j + 1, 4, item.ItemTaoBaoPrice)
            sheet.write(j + 1, 5, str(item.last_update_timestamp))
            sheet.write(j + 1, 6, item.ItemLink)
        excel.save("/home/ggfilm/Documents/taobao-excel/PriceTrace-{0}.xls".format(current_time))

        msg.attach_file("/home/ggfilm/Documents/taobao-excel/PriceTrace-{0}.xls".format(current_time))
        msg.send()
        print >> f, u"邮件发送成功".encode('utf-8')
    f.close()


if __name__ == '__main__':
    main()
