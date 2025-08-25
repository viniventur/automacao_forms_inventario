from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

import warnings
warnings.filterwarnings('ignore')

def chrome():
   
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')


    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver