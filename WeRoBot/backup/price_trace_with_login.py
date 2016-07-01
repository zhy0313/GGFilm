#! /usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main(target_url):
    try:
        new_driver = webdriver.Chrome()
        new_driver.set_window_size(1366, 768)
        try:
            print u'模拟登录淘宝网'
            new_driver.get(target_url)
            try:
                site_nav_sign = WebDriverWait(new_driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'site-nav-sign'))
                )
                login_link = WebDriverWait(site_nav_sign, 10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
                )[0]
                login_link.click()
                try:
                    login_switch = WebDriverWait(new_driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'login-switch'))
                    )
                    login_static = WebDriverWait(login_switch, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'static'))
                    )
                    login_static.click()
                    username_input_field = WebDriverWait(new_driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'username-field'))
                    )
                    username_input_box = WebDriverWait(username_input_field, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'input'))
                    )
                    username_input_box.send_keys(u'')
                    password_input_field = WebDriverWait(new_driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'pwd-field'))
                    )
                    password_input_box = WebDriverWait(password_input_field, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'input'))
                    )
                    password_input_box.send_keys('')
                    login_button = WebDriverWait(new_driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'J_SubmitStatic'))
                    )
                    login_button.click()
                    print u'登录成功...'
                except NoSuchElementException, e:
                    raise e
            except NoSuchElementException, e:
                raise e
        except TimeoutException, e:
            raise e
    except WebDriverException, e:
        raise e


if __name__ == '__main__':
    url = 'https://www.taobao.com/'
    main(url)
