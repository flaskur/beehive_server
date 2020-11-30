from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import unicodedata
import os

GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

def scrapeRedfin(house_num, street_name, zipcode):
	# try:
		print('redfin')
		address = f'{house_num} {street_name} {zipcode}'.lower()

		chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', 'chromedriver')
		chrome_options = Options()
		chrome_options.binary_location = chrome_bin
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.add_argument("--test-type")

		browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
		# browser = webdriver.Chrome(ChromeDriverManager().install())

		url = 'https://www.redfin.com/'
		browser.get(url)

		print(browser.current_url)

		wait = WebDriverWait(browser, 10)


		h = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'html')))
		print(browser.execute_script('return arguments[0].innerText', h))

		# search_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#search-box-input')))
		# search_field.send_keys(address)

		# address_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ExpandedResults div.expanded-section div.expanded-row-content a.item-title')))
		# browser.execute_script('arguments[0].click()', address_link)

		# MAIN RESULTS PAGE

		parcel_id = ''
		estimate = ''
		beds = ''
		bath = ''
		square_footage = ''
		stories = ''
		lot_size = ''
		style = ''
		year_built = ''
		year_renovated = ''
		county = ''

		# TOP STATISTICS
		try:
			# inconsistent, could be 4 or 5 values if "last sold price" exists
			main_statistics = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-rf-test-id="abp-homeinfo-homemainstats"]')))

			estimate = browser.execute_script('return arguments[0].children[0].children[0].innerText', main_statistics)
			# beds = browser.execute_script('return arguments[0].children[1].children[0].innerText', main_statistics)
			# baths = browser.execute_script('return arguments[0].children[2].children[0].innerText', main_statistics)
			# square_footage = browser.execute_script('return arguments[0].children[3].children[0].children[0].innerText', main_statistics)
			# price_per_square_footage = browser.execute_script('return arguments[0].children[3].children[0].children[2].innerText', main_statistics)
		except Exception as err:
			print(err, 'failed top statistics')

		# BOTTOM STATISTICS
		try:
			facts_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.median-values div.facts-table')))

			beds = browser.execute_script('return arguments[0].children[0].children[1].innerText', facts_table)
			baths = browser.execute_script('return arguments[0].children[1].children[1].innerText', facts_table)
			square_footage = browser.execute_script('return arguments[0].children[2].children[1].innerText', facts_table)
			stories = browser.execute_script('return arguments[0].children[3].children[1].innerText', facts_table)
			lot_size = browser.execute_script('return arguments[0].children[4].children[1].innerText', facts_table)
			style = browser.execute_script('return arguments[0].children[5].children[1].innerText', facts_table)
			year_built = browser.execute_script('return arguments[0].children[6].children[1].innerText', facts_table)
			year_renovated = browser.execute_script('return arguments[0].children[7].children[1].innerText', facts_table)
			county = browser.execute_script('return arguments[0].children[8].children[1].innerText', facts_table)
			parcel_id = browser.execute_script('return arguments[0].children[9].children[1].innerText', facts_table)
		except Exception as err:
			print(err, 'failed bottom statistics')

		scrape_info = dict(
			error=False,
			url=browser.current_url,
			parcel_id=parcel_id,
			estimate=estimate,
			market_value=estimate,
			beds=beds,
			baths=baths,
			square_footage=square_footage,
			stories=stories,
			lot_size=lot_size,
			style=style,
			year_built=year_built,
			year_renovated=year_renovated,
			county=county
		)

		browser.quit()
		return scrape_info
	# except Exception as err:
	# 	print(err)
	# 	return {
	# 		'error': True
	# 	}


# info1 = scrapeRedfin('2451', 'ellisonwoods ave', '84121')
# print(info1)

# info2 = scrapeRedfin('4068', 's 3200 w', '84119')
# print(info2)

# info3 = scrapeRedfin('9061', 'greenhills dr', '84093')
# print(info3)

# info4 = scrapeRedfin('241', 'n vine st 701e', '84103')
# print(info4)

# should fail
# info5 = scrapeRedfin('5098', 's 5625 w', '84118')
# print(info5)

# info6 = scrapeRedfin('1709', 'n 2230 w', '84043')
# print(info6)

# info7 = scrapeRedfin('612', 'n main st', '84004')
# print(info7)

# info8 = scrapeRedfin('155', 'e center st', '84004')
# print(info8)

