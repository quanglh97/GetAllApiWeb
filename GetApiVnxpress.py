from bs4 import BeautifulSoup
from time import sleep
import time
import random
from selenium import webdriver
import selenium
import io, json 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pychrome
from bs4 import BeautifulSoup

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType

import string
import logging
import threading
import time
import concurrent.futures
import random
import itertools
import sqlite3
from datetime import datetime

from enum import Enum

#################################################################################
#import lib for database
from sqlalchemy import create_engine, Integer, JSON, Column, Sequence, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create all tables derived from the EntityBase object

engine = create_engine("sqlite:///GET_API_DATABASE.db", echo=True)
EntityBase = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



options = Options()
options.add_argument("--remote-debugging-port=8000")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('window-position=0,0')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.headless = False

# add acceptInsecureCerts
capabilities = options.to_capabilities()
capabilities['acceptInsecureCerts'] = True

PROXY = "192.99.56.22:443"

prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = PROXY
prox.socks_proxy = PROXY
prox.ssl_proxy = PROXY

options.Proxy = prox
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')



class Api(EntityBase):
    __tablename__ = "API"
    id = Column(Integer, Sequence("api_id_seq"), primary_key=True, nullable=False)
    domain_id = Column(Integer, nullable=False)
    request = Column(JSON, nullable=True)
    response = Column(JSON, nullable=True)
    timeReq = Column(DateTime, nullable=True)
    timeRes = Column(DateTime, nullable=True)

EntityBase.metadata.create_all(engine)




def stringGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def stringGeneratorTopic():
    content = ["covid", 'bongda', 'thoi tiet', 'truyen tranh', 'phim', 'ảnh', 'youtube', 'facebook', 'giàu', 'biển đảo']
    r = random.randint(0, len(content))
    return content[r]

def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def ctrlClickElement(element, driver):
    b = driver.find_element_by_xpath(xpath_soup(element))
    action = webdriver.ActionChains(driver)
    if b.is_displayed():
        action.move_to_element(b).perform()
        sleep(1)
        action.key_down(Keys.LEFT_CONTROL).click(b).perform()
        sleep(3)
        print(b)

def behaviorAction(element, action):
    try:
        action.move_to_element(element).perform()
    except Exception as e:
        print("except move to element: ", e)
        return 
        #action.move_to_element(element).perform()
#check href to click
    # try: 
    #     if element.get_attribute('href'):
    #         link = element.get_attribute('href') 
    #         print(element.tag_name, link)
    #         if "http://" in link or "https://" in link:
    #             if url not in link or link in listHrefMain:
    #                 return
    #         listHref.append(link)
    #         listHrefMain.append(link)
    #         # action.key_down(Keys.LEFT_CONTROL).click(element).perform()
    #         # r = random.uniform(5, 13)
    #         # sleep(r)
    #         # #close new tab
    #         # try:
    #         #     while len(driver.window_handles) > 1:
    #         #         driver.switch_to.window(driver.window_handles[1])
    #         #         #xu ly tiếp với sub link
    #         #         r = random.uniform(2, 4)
    #         #         sleep(r)
    #         #         #actionForTab(depth + 1)
    #         #         winHandleBefore = driver.window_handles[0]
    #         #         driver.close()
    #         #         driver.switch_to.window(winHandleBefore)
    #         # except Exception as e:
    #         #     print("close new tab", e)

    #     # elif element.tag_name == 'input' and element.get_attribute('type') == 'text':
    #     #     action.click(element).send_keys(stringGeneratorTopic()).perform()
    #     #     actionC = ActionChains(driver)
    #     #     actionC.click(element).key_down(Keys.CONTROL).key_down(Keys.ENTER).perform()
    #     #     sleep(3)
    #     #     try:
    #     #         while len(driver.window_handles) > 1:
    #     #             driver.switch_to.window(driver.window_handles[1])
    #     #             #xu ly tiếp với sub link
    #     #             r = random.uniform(2.123, 5.234)
    #     #             sleep(r)
    #     #             #actionForTab(depth + 1)
    #     #             winHandleBefore = driver.window_handles[0]
    #     #             driver.close()
    #     #             driver.switch_to.window(winHandleBefore)
    #     #             sleep(3)
    #     #     except Exception as e:
    #     #         print("close new tab input ", e)
    # except Exception as e:
    #     print('check href to click ', e)
    #     return

#behavioor action for input element
def behaviorActionInput(element, action, driver, listHref):
    try:
        action.move_to_element(element).perform()
    except Exception as e:
        action.move_to_element(element).perform()


def actionForTab(driver, url, typeElement):
    ids = driver.find_elements_by_xpath('/html/body/*')#("//*")
    for ii in ids:
        action = webdriver.ActionChains(driver)
        try:
            print(ii.tag_name) 
            if ii.is_displayed():
                if typeElement == ELEMENT.HREF:
                    behaviorAction(ii, action)
                # elif typeElement == ELEMENT.INPUT:
                #     behaviorActionInput(ii, action, driver, url, lisHref)
            # else:
            #     stackElement = []
            #     stackElement.append(ii)
            #     iiTemp = ii
            #     ii_parent = iiTemp.find_element_by_xpath('..')
            #     while True:
            #         if len(stackElement) == 0:
            #             break
            #         print("______", ii_parent.tag_name)
            #         if ii_parent.is_displayed():
            #             action = webdriver.ActionChains(driver)
            #             action.move_to_element(ii_parent).perform()
            #             # if ii_parent.get_attribute('href') is None or '#' in ii_parent.get_attribute('href'):
            #             #     action.click(ii_parent).perform()
            #             ii_parent = stackElement.pop()
            #             if not ii_parent.is_displayed():
            #                 break
            #         else:
            #             stackElement.append(ii_parent)
            #             iiTemp = ii_parent
            #             ii_parent = iiTemp.find_element_by_xpath('..')

            #         if ii.is_displayed() or ii_parent.tag_name == 'body' or ii_parent.tag_name == 'head' or ii_parent.tag_name == 'html':
            #             break

            #     if ii.is_displayed():
            #             if typeElement == ELEMENT.HREF:
            #                 behaviorAction(ii, action, driver, url, listHref)
            #             elif typeElement == ELEMENT.INPUT:
            #                 behaviorActionInput(ii, action, driver, url, lisHref)  
        except Exception as e:
            print('except: ', e)
            return
            #sleep()

#actionForTab(0)
class ELEMENT(Enum):
    HREF = 1
    INPUT = 2

def runInDepth(depth, driver, url, href, listHrefMain):
    if depth < 0:
        return
    sublistHref = []
    #sublistHref.append(href)

    # if "http://" in href or "https://" in href:
    #     if url not in href or href == url[:-1]:
    #         return

    # if '/' in href and url not in href:
    #     if url[-1] == '/':
    #         href = url[:-1] + href

    try:      
        #driver = webdriver.Chrome(executable_path=r"C:\Users\HLC_2021\Desktop\chromedriver.exe", options=options)          
        driver.get(href)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        href_tags = soup.find_all(href=True)
        for a in href_tags:
            if "http://" in a['href'] or "https://" in a['href']:
                if url not in a['href'] or a['href'] == url[:-1]:
                    continue
            if "javascript:" in a['href']:
                continue
            if '/' in a['href'] and url not in a['href']:
                if url[-1] == '/':
                    a['href'] = url[:-1] + a['href']
            if a['href'] == url[:-1]:
                continue

            if a['href'] not in listHrefMain:
                listHrefMain.append(a['href'])
                sublistHref.append(a['href'])


        actionForTab(driver, href, ELEMENT.HREF)
        depth = depth - 1
    except Exception as e:
        print("for run with href: ", e)
        driver.

    for subHref in sublistHref:
        runInDepth(depth, driver, url, subHref, listHrefMain)

def funtionForHrefElement(depth, url = None):
    # Setup a database connection. Using in-memory database here.
    try:
        conn = sqlite3.connect('GET_API_DATABASE.db')
        cur = conn.cursor()
        query = "SELECT DOMAIN.id FROM DOMAIN where DOMAIN.domain ==?;"
        domain_id = cur.execute(query, [url,]).fetchall()[0][0]
    except Exception as e:
        print("check domain in database: ", e)
        return 

    ####################################################################################

    driver = webdriver.Chrome(executable_path=r"C:\Users\HLC_2021\Desktop\chromedriver.exe", options=options)
    #url = "https://vnexpress.net/"
    api = {}

    def output_on_start(**kwargs):
        if 'css' in kwargs["request"]['url']:
            return
        elif 'js' in kwargs["request"]['url']:
            return
        elif 'png;' in kwargs["request"]['url']:
            return
        elif 'jpeg;' in kwargs["request"]['url']:
            return
        elif 'jpg;' in kwargs["request"]['url']:
            return
        elif 'data:image' in kwargs["request"]['url']:
            return
        # ts = int(kwargs["timestamp"])
        # timeRequest = datetime.utcfromtimestamp(ts)
        timeRequest = datetime.now()
        api[kwargs['requestId']] = [kwargs["request"], timeRequest]   

    def output_on_finish(**kwargs):
        if kwargs['requestId'] in api.keys():
            # ts = int(kwargs["timestamp"])
            # timeResponse = datetime.utcfromtimestamp(ts)
            timeResponse = datetime.now()
            api[kwargs['requestId']].append(kwargs["response"])
            api[kwargs['requestId']].append(timeResponse)
            item = Api()
            item.domain_id = domain_id
            item.request = api[kwargs['requestId']][0]
            item.response = api[kwargs['requestId']][2]
            item.timeReq = api[kwargs['requestId']][1]
            item.timeRes = api[kwargs['requestId']][3]
            session.add(item)
            session.commit() 
        else:
            print('output_on_finish: not have request', kwargs['requestId'])

    #devtool to listen request-response
    dev_tools = pychrome.Browser(url="http://localhost:8000")
    tabs = dev_tools.list_tab()
    for tab in tabs:
        if tab is None:
            tab = browser.new_tab()
        else:
            tab = tabs[0]
    tab.start()

    tab.call_method("Network.enable", _timeout = 20)
    tab.set_listener("Network.requestWillBeSent", output_on_start)
    tab.set_listener("Network.responseReceived", output_on_finish)

    listHrefMain = []
    listHrefMain.append(url)
    runInDepth(depth, driver, url, url, listHrefMain)

    # listHref = []
    # listHref.append(url)

    # try:
    #     # driver.get(url)
    #     # soup = BeautifulSoup(driver.page_source,'html.parser')
    #     # #run action for href
    #     # actionForTab(driver, url, listHref, ELEMENT.HREF)
    #     for href in listHref:
    #         #xu ly href truoc khi get
    #         if '/' in href and url not in href:
    #             if url[-1] == '/':
    #                 href = url[:-1] + href
    #         try:                
    #             driver.get(href)
    #             #soup = BeautifulSoup(driver.page_source,'html.parser')
    #             actionForTab(driver, href, listHref, ELEMENT.HREF)
    #         except Exception as e:
    #             print("for run with href: ", e)
    #     print(listHref)
    # except Exception as e:
    #     print("url main: ", e)
      
        
# print("Main    : before creating thread")
# threadHref = threading.Thread(target=funtionForHrefElement, args=(1, "https://vnexpress.net/",), daemon=True)
# threadHref.start()
# # threadInput = threading.Thread(target=funtionForInputElement, args=("adf",), daemon=True)
# # threadInput.start()
# print("Main    : before running thread")

# print("quang dep trai nhat vu tru")
# print("Main    : wait for the thread to finish")
# threadHref.join()
# # threadInput.join()
# print("Main    : all done")