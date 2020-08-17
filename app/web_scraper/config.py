from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_chrome_driver(path="/home/ojay/chromedriver_linux64/chromedriver",incognito=False, headless=False):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    if incognito:
         options.add_argument('--incognito')
    if headless:
         options.add_argument('--headless')
    return webdriver.Chrome(path, chrome_options=options)    