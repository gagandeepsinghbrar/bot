from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
import urlparse
import pickle
import sys
import os
import re
dirname, filename = os.path.split(os.path.abspath(__file__))
today = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
transactions = 10
# # necessary ingredients.
profiles = []
driver = webdriver.Chrome('./chromedriver')


def print_message(msg):
    print('=========================')
    print('    ' + msg + '    ')


# grab the users messaged.
with open('profiles.data', 'rb') as filehandle:
    profiles = pickle.load(filehandle)
    print_message('Number of swipes so far : {}'.format(str(len(profiles))))


def check_backup_needed():
    global transactions
    if transactions >= 5:
        f_name = today + '.data'
        with open(dirname + '/backups/' + f_name, 'wb') as f:
            pickle.dump(profiles, f)
            transactions = 0


def login(username, password):
    driver.get('https://pof.com/login')
    time.sleep(1)
    driver.find_element_by_id('onetrust-accept-btn-handler').click()
    driver.find_element_by_id('login-username').send_keys(username)
    driver.find_element_by_id('login-password').send_keys(password)
    driver.find_element_by_id('login-submit').click()
    time.sleep(3)


def go_to_meet_me():
    driver.find_element_by_id('top-nav-meetme').click()
    time.sleep(2)

def race_ok(race_text):
    races = ['black']
    for race in races:
        if race in race_text:
            return False
    return True

def height_ok(height_text):
    try:
        height_in_cm = int(re.compile("([0-9]+cm)").search(height_text).groups()[0][:3])
    except:
        return True
    return height_in_cm < 172

def body_ok(body_text):
    if 'BBW body' in body_text or 'A Few Extra Pounds' in body_text:
        return False
    return True

def send_message_or_swipe_left():
    global transactions
    transactions = transactions + 1
    actions = ActionChains(driver)
    time.sleep(2)
    element = driver.find_element_by_css_selector('.card-1 .meetmeimage')
    a_element = driver.find_element_by_css_selector(
        '.card-1 .meetmeimage a').get_attribute('href')
    parsed = urlparse.urlparse(a_element)
    current_profile = urlparse.parse_qs(parsed.query)['profile_id']
    if current_profile not in profiles:
        actions.move_to_element(element).click().perform()
        profiles.append(current_profile)
        time.sleep(2)
        race = driver.find_element_by_id('attributelist-item-ethnicity')
        height = driver.find_element_by_id('attributelist-item-height')
        body = driver.find_element_by_id('attributelist-item-bodyType')
        # replace with biased messaging flag.
        if race_ok(race.text) and height_ok(height.text) and body_ok(body.text):
            driver.find_element_by_id(
                'text-area-element').send_keys("You're cute. \n How's it going! :)")
            driver.find_element_by_id('profile-message-submit').click()
            # update profile database.
            with open('profiles.data', 'wb') as f:
                pickle.dump(profiles, f)
    else:
        cross = driver.find_element_by_id('meetmevotebutton-no')
        actions.move_to_element(cross).click().perform()


try:
    login(sys.argv[1], sys.argv[2])
except:
    driver.quit()

while True:
    time.sleep(2)
    go_to_meet_me()
    driver.refresh()
    time.sleep(1)
    send_message_or_swipe_left()
    time.sleep(1)