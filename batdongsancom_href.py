from bs4 import BeautifulSoup
from time import sleep
import time
import random
from selenium import webdriver
import selenium
import io, json 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timezone
import pychrome
import pika
import sys
import requests


new_post = {}

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.headless = False
options.add_argument('window-position=0,0')
options.add_argument("--window-size=1024,720")
options.add_argument("--start-maximized")

page = 0

origin = "https://batdongsan.com.vn/nha-dat-ban/p"

driver = webdriver.Chrome(executable_path=r"C:\Users\HLC_2021\Desktop\chromedriver.exe", options=options)

while True:
    page += 1
    url = origin + str(page)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    href_div_tab = soup.findAll('div', class_=['product-item'])
    if len(href_div_tab) == 0:
        driver.quit()
        break
    for div in href_div_tab:
        a = div.find('a', {'class':'wrap-plink'})
        new_post = {}
        new_post['domain'] = 'https://batdongsan.com.vn/'
        new_post['category'] = ''
        new_post['post_id'] = ''
        new_post['post_url'] = a.get('href')
        new_post['publish_time'] = ''
        new_post['post_source'] = 'https://batdongsan.com.vn/'
        new_post['title'] = a.get('title')
        new_post['content'] = ''
        new_post['author'] = {}
        new_post['real_estate'] = {}
        new_post['raw'] = ''
        message = json.dumps(new_post)
        print(new_post)
    print('-----------------------')