#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrom_data_path = '/Users/gs/michael/app/chrome/user_data';
chrom_driver_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
driver = webdriver.Chrome()
driver.get("https://login.aliexpress.com/user/seller/login?bizSegment=CSP&return_url=http://csp.aliexpress.com/")
username = "zhm1990123@163.com"
password = "123.123.Meng"


def do_login():
    login_name_input = driver.find_element(By.ID, 'loginName')
    login_name_input.send_keys(username)

    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(password)

    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.text == "登录":
            login_button = button
    
    if login_button.is_enabled is False:
        driver.execute_script("arguments.disabled = false", login_button)
        time.sleep (2)

    login_button.click()


def do_session_login():
    options = Options()
    arg = "user-data-dir=" + chrom_data_path
    options.add_argument(arg)  # 指定Chrome的用户数据目录
    options.add_argument("--no-startup-window")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(chrom_driver_path)
    driver = webdriver.Chrome(service=service, options=options)


def get_best_sell_product():
    driver.find_element(By.NAME,"生意参谋").click()
    driver.find_element(By.NAME,"商品排行").click()
    # 支付榜、访客榜、收藏榜、加购榜
    # Top 10
    paid_goods_ids = get_goods_id("支付榜")
    visid_goods_ids = get_goods_id("访客榜")
    collect_goods_ids = get_goods_id("收藏榜")
    carted_goods_ids = get_goods_id("加购榜")
    
    ids = [paid_goods_ids,visid_goods_ids,collect_goods_ids,carted_goods_ids]
    return ids



def get_goods_id(type):
    driver.find_element(By.NAME,type).click()
    time.sleep(5)
    goods_id_span_list =  driver.find_elements(By.CLASS_NAME,"ait-typography ait-typography-ellipsis ait-typography-single-line ait-product-ellipsis ait-product-subText")
    ids = []
    for i in range(10):
        ## ID: 1005008123805928/1005008683792606
        id = ''.join(filter(str.isdigit, goods_id_span_list[i]))
        ids.append(id) 
    return ids


def do_marketing(ids):
    driver.find_element(By.NAME,"营销").click()
    driver.find_element(By.NAME,"客户营销").click()
    driver.find_element(By.NAME,"新建自定义营销计划").click()
    driver.find_element(By.NAME,"选择店铺Code").click()
    driver.find_element(By.NAME,"全选").click()
    driver.find_element(By.NAME,"确定").click()

    driver.find_element(By.NAME,"选择商品").click()
    product_dialog = driver.find_element(By.CLASS_NAME,"crm-product-dialog-ctrl")
    inputs = product_dialog.find_elements(By.TAG_NAME,"input")
    for input in inputs:
        if input.get_attribute("placeholder") == "请输入商品ID":
            for id in ids:
                input.send_keys(id)
                driver.find_element(By.CLASS_NAME,"next-checkbox-input").click()
    
    driver.find_elements(By.CLASS_NAME,"next-btn next-medium next-btn-primary").click()
    driver.find_element(By.CLASS_NAME,"next-btn-helper").click()
    

def main():
    ## do_login()
    do_session_login()
    best_sells = get_best_sell_product()
    for item in best_sells[:4]:
        do_marketing(item)



if __name__ == "__main__":
    main()