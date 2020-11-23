from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unicodedata

def scrapeWasatch(house_num, street_name):
	try:
		address = f'{house_num} {street_name}'.lower()

		options = Options()
		options.headless = True
		browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # headless mode
		# browser = webdriver.Chrome(ChromeDriverManager().install()) # opens browser

		url = 'https://www.wasatch.utah.gov/Services/Information-Lookup-Services/Property-Tax-Information-Lookup/Current-Year-Property-Tax-Lookup'
		browser.get(url)

		wait = WebDriverWait(browser, 2)

		property_address_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#dnn_ctr1237_DynamicViews_dgSearchField_SearchTextTextBox_3')))
		browser.execute_script('arguments[0].value = arguments[1]', property_address_field, address)

		search_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#dnn_ctr1237_DynamicViews_SearchImageButton')))
		browser.execute_script('arguments[0].click()', search_button)

		table_rows = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'table#dnn_ctr1237_DynamicViews_dlReport tbody tr')))
		table_rows_length = browser.execute_script('return arguments[0].length', table_rows)

		# error handling, no results
		if table_rows_length <= 2:
			return {
				'error': True
			}

		view_details_link = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table#dnn_ctr1237_DynamicViews_dlReport tbody tr td p a')))
		browser.execute_script('arguments[0].click()', view_details_link)

		# should be on main tax page
		tax_year = ''
		parcel_id = ''
		serial_id = ''
		entry_id = ''
		owner = ''
		address = ''
		tax_district = ''
		tax_district_rate = ''
		acreage = ''
		market_value = ''
		taxable_value = ''
		land_value = ''
		improvements_value = ''
		tax_charge = ''
		penalties_charged = ''
		special_charged = ''
		tax_payments = ''
		tax_abated = ''
		taxes_balance_due = ''
		escrow_processing_company = ''
		property_address = ''
		square_footage = ''
		year_built = ''
		back_tax_amount = ''
		review_date = ''
		legal_taxing_description = ''

		try:
			table_body = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#printableArea table tbody')))

			tax_year = browser.execute_script('return arguments[0].children[1].children[1].innerText', table_body)
			parcel_id = browser.execute_script('return arguments[0].children[2].children[1].innerText', table_body)
			serial_id = browser.execute_script('return arguments[0].children[3].children[1].innerText', table_body)
			entry_id = browser.execute_script('return arguments[0].children[4].children[1].innerText', table_body)
			owner = browser.execute_script('return arguments[0].children[5].children[1].innerText', table_body)
			owner2 = browser.execute_script('return arguments[0].children[6].children[1].innerText', table_body)
			address = browser.execute_script('return arguments[0].children[7].children[1].innerText', table_body)
			tax_district = browser.execute_script('return arguments[0].children[8].children[1].innerText', table_body)
			tax_district_rate = browser.execute_script('return arguments[0].children[9].children[1].innerText', table_body)
			acreage = browser.execute_script('return arguments[0].children[10].children[1].innerText', table_body)
			market_value = browser.execute_script('return arguments[0].children[11].children[1].innerText', table_body)
			taxable_value = browser.execute_script('return arguments[0].children[12].children[1].innerText', table_body)
			land_value = browser.execute_script('return arguments[0].children[13].children[1].innerText', table_body)
			improvements_value = browser.execute_script('return arguments[0].children[14].children[1].innerText', table_body)
			tax_charge = browser.execute_script('return arguments[0].children[15].children[1].innerText', table_body)
			penalties_charged = browser.execute_script('return arguments[0].children[16].children[1].innerText', table_body)
			special_charged = browser.execute_script('return arguments[0].children[17].children[1].innerText', table_body)
			tax_payments = browser.execute_script('return arguments[0].children[18].children[1].innerText', table_body)
			tax_abated = browser.execute_script('return arguments[0].children[19].children[1].innerText', table_body)
			taxes_balance_due = browser.execute_script('return arguments[0].children[20].children[1].innerText', table_body)
			escrow_processing_company = browser.execute_script('return arguments[0].children[21].children[1].innerText', table_body)
			property_address = browser.execute_script('return arguments[0].children[22].children[1].innerText', table_body)
			square_footage = browser.execute_script('return arguments[0].children[23].children[1].innerText', table_body)
			year_built = browser.execute_script('return arguments[0].children[24].children[1].innerText', table_body)
			back_tax_amount = browser.execute_script('return arguments[0].children[25].children[1].innerText', table_body)
			review_date = browser.execute_script('return arguments[0].children[26].children[1].innerText', table_body)
			legal_taxing_description = browser.execute_script('return arguments[0].children[27].children[1].innerText', table_body)
		except Exception as err:
			print(err, 'failed detail scrape')


		scrape_info = dict(
			error=False,
			county='Wasatch',
			url=browser.current_url,
			tax_year=tax_year,
			parcel_id=parcel_id,
			serial_id=serial_id,
			entry_id=entry_id,
			owner=owner,
			address=address,
			tax_district=tax_district,
			tax_district_rate=tax_district_rate,
			acreage=acreage,
			market_value=market_value,
			taxable_value=taxable_value,
			land_value=land_value,
			improvements_value=improvements_value,
			tax_charge=tax_charge,
			penalties_charged=penalties_charged,
			special_charged=special_charged,
			tax_payments=tax_payments,
			tax_abated=tax_abated,
			taxes_balance_due=taxes_balance_due,
			escrow_processing_company=escrow_processing_company,
			property_address=property_address,
			square_footage=square_footage,
			year_built=year_built,
			back_tax_amount=back_tax_amount,
			review_date=review_date,
			legal_taxing_description=legal_taxing_description
		)

		return scrape_info
	except Exception as err:
		return {
			'error': True
		}


# info1 = scrapeWasatch('290', 'w 300 s')
# print(info1)

# info2 = scrapeWasatch('2085', 'w midway ln')
# print(info2)

# info3 = scrapeWasatch('1094', 'n turnberry crt')
# print(info3)

# info4 = scrapeWasatch('12286', 'n ross creek dr')
# print(info4)

# info5 = scrapeWasatch('377', 'e keetly station cir')
# print(info5)

'''
290 w 300 s 84032
2085 w midway ln 84032
1094 n turnberry ct 84049
12286 ross creek dr 84036
377 e keetly station cir 84036
'''

# the search query is sensitive to the address input, if you are slightly off, it might not register like with ct -> crt
# final page is well formatted and very straightforward, doesn't require excessive try except blocks