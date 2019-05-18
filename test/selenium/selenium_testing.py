''' pip install selenium '''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

'''
tests:
    registering
    creating an idea
    leaderboard
    voting on an idea
    logging out
'''
def register(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    links = driver.find_elements_by_tag_name('a')
    registrationPage = [link for link in links if link.text == 'Sign Up'][0]

    registrationPage.click()
    time.sleep(3)

    randomNumber = str(random.randint(0,999999))
    field = driver.find_element_by_id("username")
    field.send_keys("SeleniumTest" + randomNumber)
    time.sleep(0.5)
    field = driver.find_element_by_id("name")
    field.send_keys("Selenium")
    time.sleep(0.5)
    field = driver.find_element_by_id("surname")
    field.send_keys("Test")
    time.sleep(0.5)
    field = driver.find_element_by_id("email")
    field.send_keys("selenium" + randomNumber + "@test.com")
    time.sleep(0.5)
    field = driver.find_element_by_id("password")
    field.send_keys("123456")
    time.sleep(0.5)
    field = driver.find_element_by_id("password2")
    field.send_keys("123456")
    time.sleep(0.5)

    driver.find_element_by_id("submit").click()
    time.sleep(3)

    links = driver.find_elements_by_tag_name('a')
    newIdeaPage = [link for link in links if link.text == 'New Idea'][0]
    newIdeaPage.click()
    time.sleep(3)

    field = driver.find_element_by_id("title")
    field.send_keys("Random Idea " + randomNumber)
    time.sleep(0.5)
    field = driver.find_element_by_id("description")
    field.send_keys("Random Idea Description " + randomNumber)
    time.sleep(0.5)
    options = driver.find_elements_by_tag_name("option")
    options[random.randint(0,len(options)-1)].click()
    time.sleep(0.5)
    field = driver.find_element_by_id("tags")
    field.send_keys(randomNumber)
    time.sleep(0.5)

    links = driver.find_elements_by_tag_name('a')
    leaderboardPage = [link for link in links if link.text == 'Leaderboard'][0]
    leaderboardPage.click()
    time.sleep(3)

    tbody = driver.find_element_by_tag_name('tbody')
    links = tbody.find_elements_by_tag_name('a')
    links[random.randint(0,len(links)-1)].click()
    time.sleep(3)

    if random.randint(0,1) == 0:
        buttons = driver.find_elements_by_tag_name('button')
        button = [button for button in buttons if button.get_attribute("title") == 'Upvote'][0]
        button.click()
    else:
        buttons = driver.find_elements_by_tag_name('button')
        button = [button for button in buttons if button.get_attribute("title") == 'Downvote'][0]
        button.click()
    time.sleep(0.5)

    listItems = driver.find_elements_by_tag_name('li')
    profile = [listItem for listItem in listItems if listItem.get_attribute('class') == 'dropdown'][0]
    profile.click()
    time.sleep(0.5)
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        print(link.get_attribute('href'))
    logout = [link for link in links if '/logout' in link.get_attribute('href')][0]
    logout.click()
    time.sleep(5)
    driver.quit()

register(url)
