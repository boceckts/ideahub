''' pip install selenium '''
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import random
import time

url = 'http://localhost:5000'

def random_trawl(url):
    driver = webdriver.Chrome()
    driver.get(url)
    while True:
        links = driver.find_elements_by_tag_name('a')
        link = random.choice(links)
        print('- Clicking ' + link.text)
        link.click()
        time.sleep(0.1)

    # driver.quit()

random_trawl(url)
