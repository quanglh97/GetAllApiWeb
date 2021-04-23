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

options = Options()
options.add_argument("--remote-debugging-port=8000")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('window-position=0,0')
options.add_argument("--start-maximized")
driver = webdriver.Chrome(executable_path=r"C:\Users\HLC_2021\Desktop\chromedriver.exe", options=options)

credentials = pika.PlainCredentials('admin', '1')
parameters = pika.ConnectionParameters('192.168.100.248', 5672, 'crawl-website', credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
    
channel.queue_declare(queue='test-queue-tiktok-airline', durable=True)

tag_list = ['vietravelairline', 'tiepvienvietravel', 'bambooairways', 'flybamboo', 'tiepvienvietbamboo', 'pacificairlines', 'flypacific', 'vietnamairline', 'vnacrew', 'vnacabincrew', 'vietnamairlinescrew ', 'flyvna', 'tiepvienvna', 'tiepvienvietnamairline', 'flyVNA', 'vietjet', 'Độiđỏ', 'vietjetair ', 'vietjetcrew', 'vietjetcabincrew', 'flyVJ', 'vzone', 'tiepvienvietjet', 'doido', 'tiepvienvj', 'bamboo']

date_time = '01.03.2021 00:00:00'
pattern = '%d.%m.%Y %H:%M:%S'
time_limit = int(time.mktime(time.strptime(date_time, pattern)))

def output_on_loaded(**kwargs):
    item_list = tab.call_method("Network.getResponseBody", requestId = kwargs['requestId'])
    item_list = item_list['body']
    if (item_list is not None) and (item_list != ''):
        try:
            item_list = json.loads(item_list)
            if 'itemList' in item_list:
                for item in item_list['itemList']:
                    t = item['createTime']
                    ts = datetime.fromtimestamp(t, timezone.utc)
                    if t < time_limit:
                        print('Late')
                    else:
                        message = json.dumps(item)
                        channel.basic_publish(
                            exchange='',    
                            routing_key='test-queue-tiktok-airline',
                            body=message,
                            properties=pika.BasicProperties(
                                delivery_mode=2,
                            ))
        except ValueError:
            pass

dev_tools = pychrome.Browser(url="http://localhost:8000")
tab = dev_tools.list_tab()[0]
tab.start()

tab.call_method("Network.enable", _timeout=20)

tab.set_listener("Network.loadingFinished", output_on_loaded)

screen_height = driver.execute_script("return window.screen.height;")
i = 1
url = "https://www.tiktok.com/tag/"
for tag in tag_list:
    page = url + tag
    i = 1
    driver.get(page)
    sleep(3)
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        sleep(random.uniform(1.5, 2))
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            sleep(3)
            break 


