from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unicodedata
import os

GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

def scrapeWeber(house_num, street_name):
	try:
		address = f'{house_num} {street_name}'.lower()

		chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', 'chromedriver')
		chrome_options = Options()
		chrome_options.binary_location = chrome_bin
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--headless')

		browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
		# browser = webdriver.Chrome(ChromeDriverManager().install())

		url = 'http://www3.co.weber.ut.us/psearch/'
		browser.get(url)

		wait = WebDriverWait(browser, 5)

		address_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#address')))
		browser.execute_script('arguments[0].value = arguments[1]', address_field, address)

		search_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'form#form3 input[value="Search"]')))
		browser.execute_script('arguments[0].click()', search_button)

		parcel_id_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[width="95%"] a')))
		browser.execute_script('arguments[0].click()', parcel_id_link)

		# MAIN PAGE
		current_url = browser.current_url

		market_value = ''
		parcel_id = ''
		owner = ''
		property_address = ''
		mailing_address = ''
		tax_unit = ''
		property_type = ''
		built_as_desc = ''
		stories = ''
		above_square_footage = ''
		basement_square_footage = ''
		square_footage = ''
		basement_percent_complete = ''
		garage_square_footage = ''
		percent_complete = ''
		exterior = ''
		roof_cover = ''
		year_built = ''
		acreage = ''

		try:
			table_body = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[width="350"] table[width="100%"] tbody')))
			market_value = browser.execute_script('return arguments[0].children[1].children[0].innerText', table_body)

			table_body2 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[width="100%"] tr:nth-child(4) td')))
			parcel_id = browser.execute_script('return arguments[0].innerText', table_body2).split('Parcel Nbr: ')[1]
		except Exception as err:
			print(err, 'failed market value or parcel id')
			
		try:
			ownership_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'td[width="120"] a')))
			browser.execute_script('return arguments[0].click()', ownership_link)

			owner_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[width="62%"] tbody')))

			owner = browser.execute_script('return arguments[0].children[0].children[1].innerText', owner_table)
			property_address = browser.execute_script('return arguments[0].children[2].children[1].innerText', owner_table)
			mailing_address = browser.execute_script('return arguments[0].children[4].children[1].innerText', owner_table)
			tax_unit = browser.execute_script('return arguments[0].children[6].children[1].innerText', owner_table)
		except Exception as err:
			print(err, 'failed ownership info')

		try:
			property_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'td[width="120"]:nth-child(4) a')))
			browser.execute_script('return arguments[0].click()', property_link)

			char_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[bgcolor="#CCCCCC"] tbody')))

			property_type = browser.execute_script('return arguments[0].children[0].children[1].innerText', char_table)
			built_as_desc = browser.execute_script('return arguments[0].children[1].children[1].innerText', char_table)
			stories = browser.execute_script('return arguments[0].children[2].children[1].innerText', char_table)
			above_square_footage = browser.execute_script('return arguments[0].children[3].children[1].innerText', char_table)
			basement_square_footage = browser.execute_script('return arguments[0].children[4].children[1].innerText', char_table)
			square_footage = browser.execute_script('return arguments[0].children[5].children[1].innerText', char_table)
			basement_percent_complete = browser.execute_script('return arguments[0].children[6].children[1].innerText', char_table)
			garage_square_footage = browser.execute_script('return arguments[0].children[7].children[1].innerText', char_table)
			percent_complete = browser.execute_script('return arguments[0].children[8].children[1].innerText', char_table)
			exterior = browser.execute_script('return arguments[0].children[9].children[1].innerText', char_table)
			roof_cover = browser.execute_script('return arguments[0].children[10].children[1].innerText', char_table)
			year_built = browser.execute_script('return arguments[0].children[11].children[1].innerText', char_table)
			acreage = browser.execute_script('return arguments[0].children[12].children[1].innerText', char_table)
		except Exception as err:
			print(err, 'failed property characteristics')
		

		scrape_info = dict(
			error=False,
			county='Weber',
			url=browser.current_url,
			market_value=market_value,
			parcel_id=parcel_id,
			owner=owner,
			property_address=property_address,
			mailing_address=mailing_address,
			tax_unit=tax_unit,
			property_type=property_type,
			built_as_desc=built_as_desc,
			stories=stories,
			above_square_footage=above_square_footage,
			basement_square_footage=basement_square_footage,
			square_footage=square_footage,
			basement_percent_complete=basement_percent_complete,
			garage_square_footage=garage_square_footage,
			percent_complete=percent_complete,
			exterior=exterior,
			roof_cover=roof_cover,
			year_built=year_built,
			acreage=acreage
		)

		browser.quit()
		return scrape_info
	except Exception as err:
		return {
			'error': True
		}


# info1 = scrapeWeber('1141', 'w excalibur way')
# print(info1)

# info2 = scrapeWeber('1930', 'brinker ave')
# print(info2)

# info3 = scrapeWeber('585', 'e 1800 n')
# print(info3)


'''
1141 w excalibur way 84401
1930 s brinker ave 84401
585 e 1800 n 84414
'''