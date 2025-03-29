#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import random
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

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
    driver.find_element(By.NAME, "商品排行").click()

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
    time.sleep(random.randint(3, 5))
    driver.find_element(By.NAME, "客户营销").click()
    time.sleep(random.randint(3, 5))
    print(driver.title) 
    btns = driver.find_elements(By.CLASS_NAME,"next-btn-helper")
    for new_biz_plan_btn in btns:
        if new_biz_plan_btn.text == "新建自定义营销计划":
            new_biz_plan_btn.click()
            break
    time.sleep(random.randint(3, 5))
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])  # 切换到新窗口
    time.sleep(random.randint(3, 5))
    print(driver.title) 
    shop_choice_btns = driver.find_elements(By.CLASS_NAME,"next-btn-helper")
    for btn in shop_choice_btns:
        if btn.text == "选择店铺Code":
            btn.click()
            break
    time.sleep(random.randint(3, 5))
    check_boxs = driver.find_elements(By.CLASS_NAME,"next-checkbox-input")
    for check_box in check_boxs:
        if check_box.get_attribute("aria-label") == "全选":
            check_box.click()
    time.sleep(random.randint(3, 5))
    shop_choice_config_btns = driver.find_elements(By.CLASS_NAME,"next-btn-helper")
    for btn in shop_choice_config_btns:
        if btn.text == "确认":
            btn.click()
            break
    time.sleep(random.randint(3, 5))

    shop_product_btns = driver.find_elements(By.CLASS_NAME,"next-btn-helper")
    for btn in shop_product_btns:
        if btn.text == "选择商品":
            btn.click()
            break
    time.sleep(random.randint(3, 5))
    product_dialog = driver.find_element(By.CLASS_NAME,"next-dialog-body")
    time.sleep(random.randint(3, 5))
    dialog_header = product_dialog.find_element(By.CLASS_NAME,"crm-product-dialog-ctrl")
    dialog_header = dialog_header.find_elements(By.CLASS_NAME,"next-icon")
    inputs = product_dialog.find_elements(By.TAG_NAME,"input")
    time.sleep(random.randint(3, 5))
    input = inputs[1]
    for id in ids:
        input.clear()
        if input.get_attribute("value") != "":
            driver.execute_script("arguments.value = '';", input)
        if input.get_attribute("value") != "":
            input.send_keys("")
        if input.get_attribute("value") != "":
            driver.execute_script("arguments.value = '';", input)
            input_value = input.get_attribute("value")  # 获取当前内容
            for _ in range(len(input_value)):
                input.send_keys(Keys.BACKSPACE) 

        input.send_keys(id)
        time.sleep(random.randint(3, 5))
        query_btns = product_dialog.find_elements(By.CSS_SELECTOR,".next-icon.next-icon-search.next-xs")
        query_btn = query_btns[0]
        query_btn.click()                
        time.sleep(random.randint(3, 5))
        check_box_container = product_dialog.find_element(By.CLASS_NAME,"next-table-cell-wrapper")
        check_box = check_box_container.find_element(By.CLASS_NAME,"next-checkbox-input")
        if check_box.tag_name == "input" and check_box.get_attribute("type") == "checkbox":
            check_box.click()

    time.sleep(random.randint(3, 5))
    goods_choice_config_btns = driver.find_elements(By.CLASS_NAME,"next-btn-helper")
    for btn in goods_choice_config_btns:
        if btn.text == "确认":
            btn.click()
            break
    time.sleep(random.randint(3, 5))
    config_btns = driver.find_elements(By.CLASS_NAME,"next-btn-helper")
    for btn in config_btns:
        if btn.text == "一键创建":
            btn.click()
            break
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def main():
    do_login()
    time.sleep(random.randint(20, 30))
    best_sells = get_best_sell_product()
    flat_list = sum(best_sells, [])
    for i in range(0, len(flat_list), 4):
        item = flat_list[i:i+4]
        print(item)
        do_marketing(item)
        time.sleep(2 + random.random() * 5)    


if __name__ == "__main__":
    main()