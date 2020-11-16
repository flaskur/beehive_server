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

	direction = street_name.split(' ', 1)[0]
	street = street_name.split(' ', 1)[1]

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

	tax_year = None
	parcel_id = None
	serial_id = None
	entry_id = None
	owner = None
	address = None
	tax_district = None
	tax_district_rate = None
	acreage = None
	market_value = None
	taxable_value = None
	land_value = None
	improvements_value = None
	tax_charge = None
	penalties_charged = None
	special_charged = None
	tax_payments = None
	tax_abated = None
	taxes_balance_due = None
	escrow_processing_company = None
	property_address = None
	square_footage = None
	year_built = None
	back_tax_amount = None
	review_date = None
	legal_taxing_description = None

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
		print(err)


	scrape_info = dict(
		error=False,
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


info1 = scrapeUtah('1709', 'n 2230 w')
print(info1)

info2 = scrapeUtah('612', 'n main st')
print(info2)

info3 = scrapeUtah('155', 'e center st')
print(info3)

'''
1709 n 2230 w 84043
612 n main st 84004
155 e center st 84004
'''