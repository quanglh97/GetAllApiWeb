from __future__ import print_function
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
from datetime import datetime

from enum import Enum

#################################################################################
#import lib for database

from elasticsearch import Elasticsearch
import uvicorn
from typing import Optional

# Create all tables derived from the EntityBase object

# session = Session(bind= engine)



# options = Options()
# options.add_argument("--remote-debugging-port=8000")
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument('window-position=0,0')
# #options.add_argument("--start-maximized")
# #options.add_argument("--window-size=1920,1080")
# options.add_experimental_option("useAutomationExtension", False)
# options.add_experimental_option("excludeSwitches",["enable-automation"])
# options.headless = False

# # add acceptInsecureCerts
# capabilities = options.to_capabilities()
# capabilities['acceptInsecureCerts'] = True

# #PROXY = "192.99.56.22:443"
# PROXY = None
# prox = Proxy()


# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')

api = {}

es = Elasticsearch(hosts='192.168.100.248', port=19200)


def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """Proxy Auth Extension
    args:
        proxy_host (str): domain or ip address, ie proxy.domain.com
        proxy_port (int): port
        proxy_username (str): auth username
        proxy_password (str): auth password
    kwargs:
        scheme (str): proxy scheme, default http
        plugin_path (str): absolute path of the extension       
    return str -> plugin_path
    """
    import string
    import zipfile

    if plugin_path is None:
        plugin_path = r'./vimm_chrome_proxyauth_plugin.zip'

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = string.Template(
    """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "${scheme}",
                host: "${host}",
                port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
          };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "${username}",
                password: "${password}"
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return plugin_path

def getProxy(options):
    #options = Options()
    options.add_argument("--remote-debugging-port=8000")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('window-position=0,0')
    #options.add_argument("--start-maximized")
    #options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    options.headless = False
    # add acceptInsecureCerts
    capabilities = options.to_capabilities()
    capabilities['acceptInsecureCerts'] = True
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    query = {
        "query": {
            "match": {
                "status": 1
                }
        }
    }
    res = es.search(index="proxy", body= query)
    listProxy = res["hits"]["hits"]
    r = random.randint(0, len(listProxy)-1)

    host = listProxy[r]["_source"]["host"]
    port = listProxy[r]["_source"]["port"]
    userName  = listProxy[r]["_source"]["authuser"]
    passWord =  listProxy[r]["_source"]["authpass"]

    proxyauth_plugin_path = create_proxyauth_extension(proxy_host=host, proxy_port=port, proxy_username=userName, proxy_password=passWord)
    options.add_extension(proxyauth_plugin_path)

    return options
    

def insertApiOfCommand(commandId, request, response, timeRequest, timeResponse):
    data = {
        'commandId': commandId,
        'request': request,
        'response': response,
        'timeRequest': timeRequest,
        'timeResponse': timeResponse,
    }
    res = es.index(index="api", body=data)
    return res['result']

def getAllCommands():
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "status": "not_run"
                        }
                    }
                ]
            }
        }
    }
    res = es.search(index="domain", body=query)
    return res["hits"]["hits"]

def updateStatusCommand(commandId, domain, url, depth, time, proxy, newStatus):
    data = {
        "domain" : domain,
        "url" : url,
        "depth" : depth,
        "time" : time,
        "proxy" : proxy,
        "status" : newStatus,
    }
    res = es.index(index="domain", id= commandId, body=data)
    return res['result']


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
        except Exception as e:
            print('except: ', e)
            return

#actionForTab(0)
class ELEMENT(Enum):
    HREF = 1
    INPUT = 2

def runInDepth(options, depth, url, href, listHrefMain, commandId = None):
    if depth < 0:
        return
    sublistHref = []

    def output_on_start(**kwargs):
        if '.css' in kwargs["request"]['url']:
            return
        elif '.js' in kwargs["request"]['url']:
            return
        elif '.png;' in kwargs["request"]['url']:
            return
        elif '.png' in kwargs["request"]['url']:
            return
        elif '.jpeg;' in kwargs["request"]['url']:
            return
        elif '.jpeg' in kwargs["request"]['url']:
            return
        elif '.jpg;' in kwargs["request"]['url']:
            return
        elif '.jpg' in kwargs["request"]['url']:
            return
        elif 'data:image' in kwargs["request"]['url']:
            return
        elif '.ico' in kwargs["request"]['url']:
            return
        elif '.svg' in kwargs["request"]['url']:
            return
        elif '.woff' in kwargs['request']['url']:
            return
        elif '.google' in kwargs['request']['url']:
            return
        elif '//fonts.' in kwargs['request']['url']:
            return
        elif '.ttf' in kwargs['request']['url']:
            return         
        timeRequest = datetime.now()
        api[kwargs['requestId']] = [kwargs["request"], timeRequest]   

    def output_on_finish(**kwargs):
        if kwargs['requestId'] in api.keys():
            print("request Id: ",kwargs['requestId'] )
            timeResponse = datetime.now()
            api[kwargs['requestId']].append(kwargs["response"])
            api[kwargs['requestId']].append(timeResponse)
            insertApiOfCommand(commandId, api[kwargs['requestId']][0], api[kwargs['requestId']][2], api[kwargs['requestId']][1], api[kwargs['requestId']][3])
        else:
            pass
            #print('output_on_finish: not have request', kwargs['requestId'])

    try:      
        driver = webdriver.Chrome(executable_path=r"C:\Users\HLC_2021\Desktop\chromedriver.exe", options=options)          
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
                #if url[-1] == '/':
                a['href'] = url[:-1] + a['href']
            if a['href'] == url[:-1]:
                continue

            if a['href'] not in listHrefMain:
                listHrefMain.append(a['href'])
                sublistHref.append(a['href'])

        actionForTab(driver, href, ELEMENT.HREF)
        depth = depth - 1
        driver.close()

    except Exception as e:
        print("for run with href: ", e)
        driver.close()

    for subHref in sublistHref:
        print("href: ", href, "subhref: ", subHref, "depth: ", depth)
        options = Options()
        options = getProxy(options)
        runInDepth(options, depth, url, subHref, listHrefMain, commandId)

def funtionForHrefElement(depth, url = None):
    # Setup a database connection. Using in-memory database here.
    listHrefMain = []
    listHrefMain.append(url)
    runInDepth(depth, url, url, listHrefMain)


def run():
    while True:
        allCommands = getAllCommands()
        if len(allCommands) <= 0:
            print("have 0 command")
            sleep(3)
            continue
        for command in allCommands:
            domain = command["_source"]["domain"]
            depth = command["_source"]["depth"]
            url = command["_source"]["url"]
            time = command["_source"]["time"]
            commandId = command["_id"]
            proxy = command['_source']["proxy"]
            if proxy == 1:
                options = Options()
                options = getProxy(options)
            else:
                options = Options()
                options.add_argument("--remote-debugging-port=8000")
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_argument('window-position=0,0')
                #options.add_argument("--start-maximized")
                #options.add_argument("--window-size=1920,1080")
                options.add_experimental_option("useAutomationExtension", False)
                options.add_experimental_option("excludeSwitches",["enable-automation"])
                options.headless = False
                # add acceptInsecureCerts
                capabilities = options.to_capabilities()
                capabilities['acceptInsecureCerts'] = True
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--ignore-ssl-errors')

            #update status command to running
            updateStatusCommand(commandId, domain, url, depth, time, proxy, "running")
            listHrefMain = []
            listHrefMain.append(url)
            runInDepth(options, depth, url, url, listHrefMain, commandId)
            #update status command to done
            updateStatusCommand(commandId, domain, url, depth, time, proxy,  "done")


if __name__ == "__main__": 
    run()