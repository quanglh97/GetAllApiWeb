import logging
import threading
import time
import concurrent.futures
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

def thread_function(name, url):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)
    driver = webdriver.Chrome(executable_path =r"C:\Users\HLC_2021\Desktop\chromedriver.exe")
    driver.get(url)
    #sleep(10)

url = "https://stackoverflow.com"

list = ["https://stackoverflow.com/questions/41354472/multi-threading-in-selenium-python",  "https://stackoverflow.com", "https://fate0.github.io/pychrome/#getting-started"]
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,list[0]), daemon=True)
    x2 = threading.Thread(target=thread_function, args=(2,list[0]), daemon=True)
    logging.info("Main    : before running thread")
    driver = webdriver.Chrome(executable_path =r"C:\Users\HLC_2021\Desktop\chromedriver.exe")
    driver.get(url)
    x.start()
    x2.start()
    sleep(10)
    logging.info("Main    : wait for the thread to finish")
    x.join()
    x2.join()
    logging.info("Main    : all done")
    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     executor.map(thread_function, range(3))