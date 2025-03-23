#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import random
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrom_data_path = '/Users/gs/michael/app/chrome/user_data';
chrom_driver_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

chrome_cmd = [
    chrom_driver_path,
    "--remote-debugging-port=9222",
    "--user-data-dir=/tmp/chrome_profile" + chrom_data_path,
    "--no-first-run"
]
subprocess.Popen(chrome_cmd)
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)

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



def get_best_sell_product():
    driver.find_element(By.NAME,"生意参谋").click()
    time.sleep(random.randint(1, 5))
    driver.find_element(By.XPATH, "//a[@title='商品排行']").click()

    # 支付榜、访客榜、收藏榜、加购榜
    # Top 10
    paid_goods_ids = get_goods_id("支付榜")
    visid_goods_ids = get_goods_id("访客榜")
    collect_goods_ids = get_goods_id("收藏榜")
    carted_goods_ids = get_goods_id("加购榜")
    
    ids = [paid_goods_ids,visid_goods_ids,collect_goods_ids,carted_goods_ids]
    return ids



def get_goods_id(type):
    group_types = driver.find_elements(By.CLASS_NAME,"ait-quick-filter-item-text")
    for group_type in group_types:
        if group_type.text == type:
            group_type.click()
            break
    time.sleep(5)
    goods_id_span_list =  driver.find_elements(By.CSS_SELECTOR,".ait-typography.ait-typography-ellipsis.ait-typography-single-line.ait-product-ellipsis.ait-product-subText")
    ids = []
    for i in range(10):
        ## ID: 1005008123805928/1005008683792606
        id = ''.join(filter(str.isdigit, goods_id_span_list[i].text))
        ids.append(id) 
    return ids


def do_marketing(ids):
    driver.find_element(By.NAME,"营销").click()
    driver.find_element(By.XPATH, "//a[@title='客户营销']").click()
    driver.find_element(By.CSS_SELECTOR,".next-btn.next-medium.next-btn-secondary").click()
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
    
    driver.find_elements(By.CSS_SELECTOR,".next-btn.next-medium.next-btn-primary").click()
    driver.find_element(By.CLASS_NAME,"next-btn-helper").click()
    

def main():
    do_login()
    time.sleep(random.randint(20, 30))
    best_sells = get_best_sell_product()
    for item in best_sells[:4]:
        do_marketing(item)
        time.sleep(2 + random.random() * 5)


if __name__ == "__main__":
    main()