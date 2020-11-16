from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unicodedata

def scrapeUtah(house_num, street_name):
	address = f'{house_num} {street_name}'.lower()

	direction = street_name.split(' ', 1)[0][0].lower()
	street = street_name.split(' ', 1)[1].lower()

	# options = Options()
	# options.headless = True
	# browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # headless mode
	browser = webdriver.Chrome(ChromeDriverManager().install()) # opens browser

	# navigate to start webpage --> avoids iframe
	url = 'http://www.utahcounty.gov/LandRecords/AddressSearchForm.asp'
	browser.get(url)

	wait = WebDriverWait(browser, 5)

	house_num_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#av_house')))
	browser.execute_script('arguments[0].value = arguments[1]', house_num_field, house_num)

	# SWITCH DIRECTION --> RADIO SELECTION?
	direction_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'select#av_dir')))
	if direction == 'e':
		east_option = browser.execute_script('return arguments[0].children[1]', direction_field)
		browser.execute_script('arguments[0].selected = true', east_option)
	elif direction == 'w':
		west_option = browser.execute_script('return arguments[0].children[2]', direction_field)
		browser.execute_script('arguments[0].selected = true', west_option)
	elif direction == 's':
		south_option = browser.execute_script('return arguments[0].children[3]', direction_field)
		browser.execute_script('arguments[0].selected = true', south_option)
	elif direction == 'n':
		north_option = browser.execute_script('return arguments[0].children[4]', direction_field)
		browser.execute_script('arguments[0].selected = true', north_option)
	else:
		print('no direction', direction)


	street_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#av_street')))
	browser.execute_script('arguments[0].value = arguments[1]', street_field, street)

	search_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="Submit"]')))
	browser.execute_script('arguments[0].click()', search_button)

	# ERROR HANDLING


	table_body = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table table tbody')))
	serial_number_link = browser.execute_script('return arguments[0].children[1].children[0].children[0]', table_body)
	browser.execute_script('arguments[0].click()', serial_number_link)

	# repeat page for serial num
	table_body = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table table tbody')))
	serial_number_link = browser.execute_script('return arguments[0].children[1].children[0].children[0]', table_body)
	browser.execute_script('arguments[0].click()', serial_number_link)

	# MAIN PAGE
	url = browser.current_url

	serial_number = None
	serial_life = None
	property_address = None
	mailing_address = None
	acreage = None
	legal_description = None

	parcel_id = None
	tax_year = None
	address = None
	owner = None
	account_type = None
	primary_use = None
	land_size = None
	land_size_square_footage = None

	improvement_number = None
	improvement_type = None
	square_footage = None
	basement_square_footage = None
	basement_square_footage_finished = None
	year_built = None
	adj_year_built = None

	quality = None
	condition = None
	exterior = None
	interior = None
	roof_type = None
	roof_cover = None
	foundation = None

	bedroom_count = None
	full_bath = None
	three_fourths_bath = None
	half_bath = None
	fireplace = None


	# scrape the main page, move to property info, move back to main page url, scrape property valuation

	try:
		table_body = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table table table tbody')))

		serial_number = browser.execute_script('return arguments[0].children[0].children[0].innerText.split("Serial Number:")[1].trim()', table_body)
		serial_life = browser.execute_script('return arguments[0].children[0].children[1].innerText.split("Serial Life:")[1].trim()', table_body)
		property_address = browser.execute_script('return arguments[0].children[2].children[0].innerText.split("Property Address:")[1].trim()', table_body)
		mailing_address = browser.execute_script('return arguments[0].children[3].children[0].innerText.split("Mailing Address:")[1].trim()', table_body)
		acreage = browser.execute_script('return arguments[0].children[4].children[0].innerText.split("Acreage:")[1].trim()', table_body)
		legal_description = browser.execute_script('return arguments[0].children[7].children[0].innerText.split("Legal Description:")[1].trim()', table_body)
		
	except Exception as err:
		print(err)


	scrape_info = dict(
		error=False,
		url=url,
		serial_number=serial_number,
		serial_life=serial_life,
		property_address=property_address,
		mailing_address=mailing_address,
		acreage=acreage,
		legal_description=legal_description
	)

	return scrape_info


info1 = scrapeUtah('1709', 'n 2230 w')
print(info1)

# info2 = scrapeUtah('612', 'n main st')
# print(info2)

# info3 = scrapeUtah('155', 'e center st')
# print(info3)

'''
1709 n 2230 w 84043
612 n main st 84004
155 e center st 84004
'''