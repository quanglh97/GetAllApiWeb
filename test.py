
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pychrome
from threading import Timer
from time import sleep
import threading
# options = Options()
# options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument('window-position=0,0')
# options.add_argument("--start-maximized")
# options.add_argument('disable-infobars')

options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=8000")
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.headless = False
driver = webdriver.Chrome(executable_path=r"C:\Users\HLC_2021\Desktop\chromedriver.exe", options=options)
driver.maximize_window()

def function(indexDriver):
    print("in thread")
    indexDriver.switch_to.window(indexDriver.window_handles[1])

dev_tools = pychrome.Browser(url="http://localhost:8000")
tab = dev_tools.list_tab()[0]


driver.get('https://vnexpress.net/')
sleep(3)
driver.get('https://www.w3schools.com/')


# action = webdriver.ActionChains(driver)

# a = driver.find_element_by_xpath('//*[@id="wrap-main-nav"]/nav/ul/li[3]/a')
# action.move_to_element(a).perform()
# action.key_down(Keys.LEFT_CONTROL).click(a).perform()

# print("before start thread")
# b = driver.find_element_by_xpath('//*[@id="wrap-main-nav"]/nav/ul/li[3]/ul/li[1]/a')
# if b.is_displayed():
#     print('b is visible')
# driver2 = driver
# x = threading.Thread(target=function, args=(driver2,), daemon=True)
# x.start()
# x.join()
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# if b.is_displayed():
#     print('b is not visible')
# driver.switch_to.window(driver.window_handles[0])
# print("finish thread main")
# sleep(30)
# print(soup)
# t = Timer(50, None)  
# t.start()  
