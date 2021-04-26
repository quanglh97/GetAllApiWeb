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

import logging
import threading
import time
import concurrent.futures
#from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_argument("--remote-debugging-port=8000")
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('window-position=0,0')
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.headless = False
driver = webdriver.Chrome(executable_path=r"C:\Users\HLC_2021\Desktop\chromedriver.exe", options=options)

queue_request = []


dev_tools = pychrome.Browser(url="http://localhost:8000")
tab = dev_tools.list_tab()[0]
tab.start()

def output_on_start(**kwargs):
    #print("type of request: ", type(kwargs["request"]['url']))
    #print("START: ", "type of kwargs: ", type(kwargs), "\n", kwargs)
    if 'css' in kwargs["request"]['url']:
        return
    elif 'js' in kwargs["request"]['url']:
        return
    #dictTemp = {kwargs["request"]['requestId']}
    queue_request.append(kwargs["request"])


def output_on_finish(**kwargs):
    #print("STOP: ","type of kwargs: ", type(kwargs), "\n", kwargs)
    pass

import itertools

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

def CtrlClickElement(element, driver):
    b = driver.find_element_by_xpath(xpath_soup(element))
    action = webdriver.ActionChains(driver)
    if b.is_displayed():
        action.move_to_element(b).perform()
        sleep(1)
        action.key_down(Keys.LEFT_CONTROL).click(b).perform()
        sleep(3)
        print(b)
        # if len(driver.window_handles) > 1:
        #     driver2 = driver
        #     driver2.switch_to_window(driver2.window_handles[1])

tab.call_method("Network.enable", _timeout = 20)
tab.set_listener("Network.requestWillBeSent", output_on_start)
tab.set_listener("Network.responseReceived", output_on_finish)

url = "https://vnexpress.net/"

#action = webdriver.ActionChains(driver)
driver.get(url)

#search = driver.find_element_by_id("keywordHeader")
# driver.find_element_by_id("keywordHeader").send_keys("qua")
# driver.find_element_by_id("keywordHeader").send_keys(Keys.RETURN)
# browserTabs = driver.window_handles

# while len(driver.window_handles) > 1:
#     driver.switch_to_window(driver.window_handles[1])
#     sleep(3)
#     driver.close()

#browserTabs[1].close()
#browserTabs[2].close()
# a = driver.find_element_by_xpath('//a[@href="https://vnexpress.net/thoi-su"]')
# action.move_to_element(a)
# action.perform()

soup = BeautifulSoup(driver.page_source,'html.parser')
# elements = soup.find_all("a")
# print("search all elements by soup\n")
# for element in elements:
#         print(element)

# CtrlClickElement(href_a_tab, driver)

ids = driver.find_elements_by_xpath("//*")
#print("search all elements by selenium\n")
#print(driver.current_window_handle)
for ii in ids:
    action = webdriver.ActionChains(driver)
    if ii.is_displayed():
        try:
            action.move_to_element(ii).perform()
        except Exception as e:
            action.move_to_element(ii).perform()
        #check href to click
        try: 
            if ii.tag_name == "a":
                link = ii.get_attribute('href') 
                if "http://" in link or "https://" in link:
                    if url not in link:
                        continue
                action.key_down(Keys.LEFT_CONTROL).click(ii).perform()
                try:
                    if len(driver.window_handles) > 1:
                        #if driver.current_window_handle == driver.window_handles[0]:
                            #switch tab
                        action = webdriver.ActionChains(driver)
                        #action.key_down(Keys.LEFT_CONTROL).key_down(Keys.TAB).key_up(Keys.CONTROL).key_up(Keys.TAB).perform()
                        action.send_keys(Keys.CONTROL, Keys.TAB).perform()
                        #sleep(5)
                        #clear new tab
                        action = webdriver.ActionChains(driver)
                        action.send_keys(Keys.LEFT_CONTROL).send_keys("w").perform()
                except Exception as e:
                    print('first err ', e)
                action = webdriver.ActionChains(driver)
                action.move_to_element(ii).perform()
        except Exception as e:
            print('second err ', e)
            continue
    print(ii) 

# threads = list()
# for a in href_a_tab:
#     CtrlClickElement(a, driver)
    #x = threading.Thread(target=CtrlClickElement, args=(a, driver), daemon=True)
    #logging.info("Main    : before running thread")
    #x.start()
    #logging.info("Main    : wait for the thread to finish")
    #threads.append(x)

# for index, thread in enumerate(threads):
#         logging.info("Main    : before joining thread %d.", index)
#         thread.join()
#         logging.info("Main    : thread %d done", index)
    
#print(queue_a)
#print("queue_request: ", queue_request)

#sleep(30)