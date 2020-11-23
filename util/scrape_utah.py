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
	try:
		address = f'{house_num} {street_name}'.lower()

		direction = street_name.split(' ', 1)[0][0].lower()
		street = street_name.split(' ', 1)[1].lower()

		options = Options()
		options.headless = True
		browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # headless mode
		# browser = webdriver.Chrome(ChromeDriverManager().install()) # opens browser

		url = 'http://www.utahcounty.gov/LandRecords/AddressSearchForm.asp'
		browser.get(url)

		wait = WebDriverWait(browser, 5)

		house_num_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#av_house')))
		browser.execute_script('arguments[0].value = arguments[1]', house_num_field, house_num)

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

		try:
			table_body = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table table tbody')))
			serial_number_link = browser.execute_script('return arguments[0].children[1].children[0].children[0]', table_body)
			browser.execute_script('arguments[0].click()', serial_number_link)

			# repeat page for serial num
			table_body = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table table tbody')))
			serial_number_link = browser.execute_script('return arguments[0].children[1].children[0].children[0]', table_body)
			browser.execute_script('arguments[0].click()', serial_number_link)
		except Exception as err:
			print(err, 'failed to find serial number link, no entry')

			return {
				'error': True
			}

		# MAIN PAGE
		property_information_url = browser.current_url
		appraisal_information_url = browser.current_url
		property_valuation_url = browser.current_url

		serial_number = ''
		serial_life = ''
		property_address = ''
		mailing_address = ''
		acreage = ''
		legal_description = ''
		parcel_id = ''
		tax_year = ''
		address = ''
		owner = ''
		account_type = ''
		primary_use = ''
		land_size = ''
		land_size_square_footage = ''
		improvement_number = ''
		improvement_type = ''
		square_footage = ''
		basement_square_footage = ''
		basement_square_footage_finished = ''
		year_built = ''
		adj_year_built = ''
		quality = ''
		condition = ''
		exterior = ''
		interior = ''
		roof_type = ''
		roof_cover = ''
		foundation = ''
		beds = ''
		full_bath = ''
		three_fourths_baths = ''
		half_baths = ''
		fireplaces = ''
		previous_market_value = ''
		market_value = ''


		# property information
		try:
			table_body = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table table table tbody')))

			serial_number = browser.execute_script('return arguments[0].children[0].children[0].innerText.split("Serial Number:")[1].trim()', table_body)
			serial_life = browser.execute_script('return arguments[0].children[0].children[1].innerText.split("Serial Life:")[1].trim()', table_body)
			property_address = browser.execute_script('return arguments[0].children[2].children[0].innerText.split("Property Address:")[1].trim()', table_body)
			mailing_address = browser.execute_script('return arguments[0].children[3].children[0].innerText.split("Mailing Address:")[1].trim()', table_body)
			acreage = browser.execute_script('return arguments[0].children[4].children[0].innerText.split("Acreage:")[1].trim()', table_body)
			legal_description = browser.execute_script('return arguments[0].children[7].children[0].innerText.split("Legal Description:")[1].trim()', table_body)

			navigation_select = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'form#page-changer select')))
			appraisal_information_option = browser.execute_script('return arguments[0].children[4]', navigation_select)
			appraisal_information_url = 'http://www.utahcounty.gov/LandRecords/' + browser.execute_script('return arguments[0].value', appraisal_information_option)
			property_valuation_option = browser.execute_script('return arguments[0].children[5]', navigation_select)
			property_valuation_url = 'http://www.utahcounty.gov/LandRecords/' + browser.execute_script('return arguments[0].value', property_valuation_option)
		except Exception as err:
			print(err, 'failed property information')


		# appraisal information
		try:
			browser.get(appraisal_information_url)

			property_information_table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table table tbody')))

			parcel_id = browser.execute_script('return arguments[0].children[1].children[0].children[1].innerText', property_information_table)
			tax_year = browser.execute_script('return arguments[0].children[1].children[0].children[2].innerText.split("Tax Year:")[1].trim()', property_information_table)
			address = browser.execute_script('return arguments[0].children[3].children[1].innerText', property_information_table)
			owner = browser.execute_script('return arguments[0].children[5].children[1].innerText', property_information_table)
			account_type = browser.execute_script('return arguments[0].children[7].children[1].innerText', property_information_table)
			primary_use = browser.execute_script('return arguments[0].children[8].children[1].innerText', property_information_table)
			land_size = browser.execute_script('return arguments[0].children[10].children[1].innerText', property_information_table)
			land_size_square_footage = browser.execute_script('return arguments[0].children[11].children[1].innerText', property_information_table)

			table1 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[width="300"] tbody')))
			table2 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[width="240"] tbody')))
			table3 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[width="140"] tbody')))

			improvement_number = browser.execute_script('return arguments[0].children[0].children[1].innerText', table1)
			improvement_type = browser.execute_script('return arguments[0].children[1].children[1].innerText', table1)
			square_footage = browser.execute_script('return arguments[0].children[2].children[1].innerText', table1)
			basement_square_footage = browser.execute_script('return arguments[0].children[3].children[1].innerText', table1)
			basement_square_footage_finished = browser.execute_script('return arguments[0].children[4].children[1].innerText', table1)
			year_built = browser.execute_script('return arguments[0].children[5].children[1].innerText', table1)
			adj_year_built = browser.execute_script('return arguments[0].children[6].children[1].innerText', table1)
			
			quality = browser.execute_script('return arguments[0].children[0].children[1].innerText', table2)
			condition = browser.execute_script('return arguments[0].children[1].children[1].innerText', table2)
			exterior = browser.execute_script('return arguments[0].children[2].children[1].innerText', table2)
			interior = browser.execute_script('return arguments[0].children[3].children[1].innerText', table2)
			roof_type = browser.execute_script('return arguments[0].children[4].children[1].innerText', table2)
			roof_cover = browser.execute_script('return arguments[0].children[5].children[1].innerText', table2)
			foundation = browser.execute_script('return arguments[0].children[6].children[1].innerText', table2)

			beds = browser.execute_script('return arguments[0].children[0].children[1].innerText', table3)
			baths = browser.execute_script('return arguments[0].children[2].children[1].innerText', table3)
			three_fourths_baths = browser.execute_script('return arguments[0].children[3].children[1].innerText', table3)
			half_baths = browser.execute_script('return arguments[0].children[4].children[1].innerText', table3)
			fireplaces = browser.execute_script('return arguments[0].children[6].children[1].innerText', table3)
		except Exception as err:
			print(err, 'failed appraisal information')


		# property valuation information
		try:
			browser.get(property_valuation_url)

			table = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[width="680"] tbody')))

			previous_market_value = browser.execute_script('return arguments[0].children[arguments[0].children.length - 1].children[1].innerText', table)
			market_value = browser.execute_script('return arguments[0].children[arguments[0].children.length - 1].children[4].innerText', table)
		except Exception as err:
			print(err, 'failed property valuation')


		scrape_info = dict(
			error=False,
			county='Utah',
			url=property_information_url,
			serial_number=serial_number,
			serial_life=serial_life,
			property_address=property_address,
			mailing_address=mailing_address,
			acreage=acreage,
			legal_description=legal_description,
			parcel_id=parcel_id,
			tax_year=tax_year,
			address=address,
			owner=owner,
			account_type=account_type,
			primary_use=primary_use,
			land_size=land_size,
			land_size_square_footage=land_size_square_footage,
			improvement_number=improvement_number,
			improvement_type=improvement_type,
			square_footage=square_footage,
			basement_square_footage=basement_square_footage,
			basement_square_footage_finished=basement_square_footage_finished,
			year_built=year_built,
			adj_year_built=adj_year_built,
			quality=quality,
			condition=condition,
			exterior=exterior,
			interior=interior,
			roof_type=roof_type,
			roof_cover=roof_cover,
			foundation=foundation,
			beds=beds,
			baths=baths,
			three_fourths_baths=three_fourths_baths,
			half_baths=half_baths,
			fireplaces=fireplaces,
			previous_market_value=previous_market_value,
			market_value=market_value
		)

		return scrape_info
	except Exception as err:
		return {
			'error': True
		}


# info1 = scrapeUtah('1709', 'n 2230 w')
# print(info1)

# info2 = scrapeUtah('612', 'n main')
# print(info2)

# info3 = scrapeUtah('155', 'e center st')
# print(info3)

'''
1709 n 2230 w 84043
612 n main st 84004
155 e center st 84004
'''