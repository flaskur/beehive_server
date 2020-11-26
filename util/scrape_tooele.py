from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unicodedata

def scrapeTooele(house_num, street_name):
	try:
		address = f'{house_num} {street_name}'.lower()

		options = Options()
		options.headless = True
		browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # headless mode
		# browser = webdriver.Chrome(ChromeDriverManager().install()) # opens browser

		url = 'https://erecording.tooeleco.org/eaglesoftware/web/login.jsp'
		browser.get(url)

		wait = WebDriverWait(browser, 10)

		enter_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[value="Enter"]')))
		browser.execute_script('arguments[0].click()', enter_button)

		accept_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[value="Accept"]')))
		browser.execute_script('arguments[0].click()', accept_button)

		house_num_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#SitusIDHouseNumber')))
		browser.execute_script('arguments[0].value = arguments[1]', house_num_field, house_num)

		street_name_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#SitusIDStreetName')))
		browser.execute_script('arguments[0].value = arguments[1]', street_name_field, street_name)

		search_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[value="Search"]')))
		browser.execute_script('arguments[0].click()', search_button)

		account_row = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table#searchResultsTable tr.tableRow1 a')))
		browser.execute_script('arguments[0].click()', account_row)

		# MAIN PAGE

		acreage = ''
		parcel_id = ''
		account_id = ''
		tax_district = ''
		year_built = ''
		square_footage = ''
		basement_square_footage = ''
		basement_square_footage_complete = ''
		status_code = ''
		owner = ''
		legal_description = ''
		entry_date = ''
		remarks = ''
		market_value = ''
		primary_taxable = ''

		try:
			table_body1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.accountSummary tbody tr td table tbody')))

			acreage = browser.execute_script('return arguments[0].children[0].innerText', table_body1).split('Acres')[1].strip()
			parcel_id = browser.execute_script('return arguments[0].children[1].innerText', table_body1).split('Parcel Number')[1].strip()
			account_id = browser.execute_script('return arguments[0].children[2].innerText', table_body1).split('Account Number')[1].strip()
			tax_district = browser.execute_script('return arguments[0].children[3].innerText', table_body1).split('Tax District')[1].strip()
			year_built = browser.execute_script('return arguments[0].children[4].innerText', table_body1).split('Year Built')[1].strip()
			square_footage = browser.execute_script('return arguments[0].children[5].innerText', table_body1).split('Above Ground SQFT')[1].strip()
			basement_square_footage = browser.execute_script('return arguments[0].children[6].innerText', table_body1).split('Basement SQFT')[1].strip()
			basement_square_footage_complete = browser.execute_script('return arguments[0].children[7].innerText', table_body1).split('Basement SQFT Complete')[1].strip()
			status_code = browser.execute_script('return arguments[0].children[8].innerText', table_body1).split('Status Code')[1].strip()
			owner = browser.execute_script('return arguments[0].children[13].innerText', table_body1).split('OwnerName')[1].strip()
			legal_description = browser.execute_script('return arguments[0].children[16].innerText', table_body1).split('Legal')[1].strip()
			entry_date = browser.execute_script('return arguments[0].children[17].innerText', table_body1).split('Entry Date')[1].strip()
			remarks = browser.execute_script('return arguments[0].children[18].innerText', table_body1).split('Remarks')[1].strip()
			
			table_body3 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table.accountSummary tbody tr td[colspan="1"] table tbody')))
			market_value = browser.execute_script('return arguments[0].children[0].children[1].innerText', table_body3)
			primary_taxable = browser.execute_script('return arguments[0].children[1].children[1].innerText', table_body3)
		except Exception as err:
			print(err, 'failed results scrape')


		scrape_info = dict(
			error=False,
			county='Tooele',
			url=browser.current_url,
			acreage=acreage,
			parcel_id=parcel_id,
			account_id=account_id,
			tax_district=tax_district,
			year_built=year_built,
			square_footage=square_footage,
			basement_square_footage=basement_square_footage,
			basement_square_footage_complete=basement_square_footage_complete,
			status_code=status_code,
			owner=owner,
			legal_description=legal_description,
			entry_date=entry_date,
			remarks=remarks,
			market_value=market_value,
			primary_taxable=primary_taxable
		)

		return scrape_info
	except Exception as err:
		return {
			'error': True
		}



# info2 = scrapeTooele('365', 'vine st')
# print(info2)

# info3 = scrapeTooele('360', 'overland rd')
# print(info3)

# info4 = scrapeTooele('770', 'fleetwood dr')
# print(info4)


'''
365 e vine st 84074
360 n overland rd 84074
770 fleetwood dr 84074
'''

# tooele query is inconsistent and will not show exact matches. you often have to exclude the direction for it to show up.