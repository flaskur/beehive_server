from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unicodedata

def scrapeZillow(house_num, street_name, zipcode):
	address = f'{house_num} {street_name} {zipcode}'
	print(f'address is {address}')
	
	# setup the browser

	# HEADLESS
	# options = Options()
	# options.headless = True
	# browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

	# ACTIVE BROWSER
	browser = webdriver.Chrome(ChromeDriverManager().install())

	# navigate to zillow search page for utah state
	url = 'https://www.zillow.com/browse/homes/ut/'
	browser.get(url)

	# access and set input field
	search_field = browser.find_element_by_css_selector('input#citystatezip')
	browser.execute_script('arguments[0].value = arguments[1]', search_field, address)

	# press search button
	search_button = browser.find_element_by_css_selector('button.zsg-search-button')
	browser.execute_script('arguments[0].click()', search_button)

	# extract all relevant information

	wait = WebDriverWait(browser, 5)
	zestimate_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.zestimate-value')))

	# zestimate_container = browser.find_element_by_css_selector('div.zestimate-value')
	zestimate = browser.execute_script('return arguments[0].innerText', zestimate_container)

	# not sure if these classes will be consistent across addresses...
	facts_and_features = browser.find_element_by_css_selector('div.ds-home-facts-and-features div.sc-fzpans')

	home_fact = browser.find_element_by_css_selector('ul.ds-home-fact-list')

	home_type = browser.execute_script('return arguments[0].children[0].children[2].innerText', home_fact)
	year_built = browser.execute_script('return arguments[0].children[1].children[2].innerText', home_fact)
	heating = browser.execute_script('return arguments[0].children[2].children[2].innerText', home_fact)
	cooling = browser.execute_script('return arguments[0].children[3].children[2].innerText', home_fact)
	parking = browser.execute_script('return arguments[0].children[4].children[2].innerText', home_fact)
	lot = browser.execute_script('return arguments[0].children[5].children[2].innerText', home_fact)
	
	# this query is inconsistent, need larger path --> might need to click more details link first
	interior_details_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.sc-19crqy3-4 div.sc-pTWqp div.sc-oVpqz')))
	interior_details_length = browser.execute('return arguments[0].children.length', interior_details_box)
	
	# the information inside of interior details is variable, so instead you should populate a dictionary with the innertext is 
	interior_details = {}

	for i in range(interior_details_length):
		element = browser.execute_script('return arguments[0].children[arguments[1]]', interior_details_box, i)
		key = browser.execute_script('return arguments[0].children[0].innerText', element)
		value = browser.execute_script('return arguments[0].children[1].innerText', element)

		interior_details[key] = value
		
	scrape_info = dict(
		error=False,
		url=browser.current_url,
		zestimate=zestimate,
		home_type=home_type,
		year_built=year_built,
		heating=heating,
		cooling=cooling,
		parking=parking,
		lot=lot,
		interior_detail=interior_details
	)

	return scrape_info


# info1 = scrapeZillow('2451', 'ellisonwoods ave', '84121')
# print(info1)

# info2 = scrapeZillow('4068', 's 3200 w', '84119')
# print(info2)

# info3 = scrapeZillow('9061', 'greenhills dr', '84093')
# print(info3)