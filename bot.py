from selenium import webdriver
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
import urlparse
import pickle
import sys
today = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
transactions = 10
# # necessary ingredients.
profiles = []
driver = webdriver.Chrome('./chromedriver')



# grab the users messaged.
with open('profiles.data', 'rb') as filehandle:
    profiles = pickle.load(filehandle)

    print('profiles are:- ',profiles)
def check_backup_needed():
	global transactions
	if transactions >= 10:
		f_name = today + '.data'
		with open(f_name, 'wb') as f:
			print('backing up now -> ',profiles)
  			pickle.dump(profiles, f)


def login(username,password):
	driver.get('https://pof.com/login')
	time.sleep(1)
	driver.find_element_by_id('onetrust-accept-btn-handler').click()
	driver.find_element_by_id('login-username').send_keys(username)
	driver.find_element_by_id('login-password').send_keys(password)
	driver.find_element_by_id('login-submit').click();
	time.sleep(3)

def go_to_meet_me():
	driver.find_element_by_id('top-nav-meetme').click();
	time.sleep(3)

def send_message_or_swipe_left():
	global transactions
	transactions = transactions + 1
	actions = ActionChains(driver)
	time.sleep(3)
	element = driver.find_element_by_css_selector('.card-1 .meetmeimage')
	a_element = driver.find_element_by_css_selector('.card-1 .meetmeimage a').get_attribute('href')
	parsed = urlparse.urlparse(a_element)
	current_profile = urlparse.parse_qs(parsed.query)['profile_id']
	print(a_element)
	if current_profile not in profiles:
		actions.move_to_element(element).click().perform()
		profiles.append(current_profile)
		time.sleep(2)
		driver.find_element_by_id('text-area-element').send_keys("You're cute. \n How's it going! :)")
		driver.find_element_by_id('profile-message-submit').click()
		# update profile database.
		with open('profiles.data', 'wb') as f:
			print('writing -> ',profiles)
	   		pickle.dump(profiles, f)
	else:
		cross = driver.find_element_by_id('meetmevotebutton-no')
		actions.move_to_element(cross).click().perform()


try:
	login(sys.argv[1],sys.argv[2])
except:
	driver.quit()

while True:
	try:
		time.sleep(5)
		go_to_meet_me()
		driver.refresh()
		time.sleep(2)
		send_message_or_swipe_left()
		time.sleep(5)
	except:
		driver.quit()

