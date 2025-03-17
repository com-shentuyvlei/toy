#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://login.aliexpress.com/user/seller/login?bizSegment=CSP&return_url=http://csp.aliexpress.com/")
##get elements from parent element using TAG_NAME

# Get element with tag name 'div'
login_name_input = driver.find_element(By.ID, 'loginName')
login_name_input.send_keys("zhm1990123@163.com")

# Get all the elements available with tag name 'p'
password_input = driver.find_element(By.ID, 'password')
password_input.send_keys("123.123.Meng")

check_input = driver.find_element(By.CSS_SELECTOR, "loginButton")
check_input.click()