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

def scrapeSalt(house_num, street_name):
	try:
		address = f'{house_num} {street_name}'.lower()

		chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', 'chromedriver')
		chrome_options = Options()
		chrome_options.binary_location = chrome_bin
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--headless')

		browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

		url = 'https://slco.org/assessor/new/searchiframe.cfm'
		browser.get(url)

		house_num_field = browser.find_element_by_css_selector('input[name="street_Num"]')
		browser.execute_script('arguments[0].value = arguments[1]', house_num_field, house_num)

		street_name_field = browser.find_element_by_css_selector('input[name="street_name"]')
		browser.execute_script('arguments[0].value = arguments[1]', street_name_field, street_name)

		submit_button = browser.find_element_by_css_selector('input#Submit')
		browser.execute_script('arguments[0].click()', submit_button)

		wait = WebDriverWait(browser, 10)

		results_white = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsWhite')))

		new_urls = []

		# iterate through white rows, if address matches, immediately move to new url
		found_count = 0
		for result in results_white:
			result_address = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[0].children[2].children[0].children[0].innerText', result)).strip().lower()
			result_address = result_address.split(' ')
			end_address = address.split(' ')

			success = True

			while len(result_address) != 0:
				if result_address[0] in end_address:
					end_address.remove(result_address.pop(0))
					# print(result_address, end_address)
				else:
					success = False
					break

			# on failure it will not add the url to new_urls
			if success:
				source = browser.execute_script('return arguments[0].children[0].getAttribute("onclick")', result)
				new_url = 'https://slco.org/assessor/new/' + source.split("'")[1]
				found_count += 1
				new_urls.append(new_url)


		results_grey = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsGrey')))

		for result in results_grey:
			result_address = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[0].children[2].children[0].children[0].innerText', result)).strip().lower()
			result_address = result_address.split(' ')
			end_address = address.split(' ')

			success = True

			while len(result_address) != 0:
				if result_address[0] in end_address:
					end_address.remove(result_address.pop(0))
					# print(result_address, end_address)
				else:
					success = False
					break

			# on failure it will not add the url to new_urls
			if success:
				source = browser.execute_script('return arguments[0].children[0].getAttribute("onclick")', result)
				new_url = 'https://slco.org/assessor/new/' + source.split("'")[1]
				found_count += 1
				new_urls.append(new_url)

		# no address match, return error
		if found_count < 1:
			return {
				'error': True
			}

		print(new_urls)

		# for now assume we take the last url?
		browser.get(new_urls[-1])

		parcel_id = ''
		owner = ''
		address = ''
		acreage = ''
		square_footage = ''
		property_type = ''
		tax_district = ''
		land_value = ''
		building_value = ''
		market_value = ''

		try:
			parcel_id_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#parcelFieldNames div div strong')))
			parcel_id = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].innerText', parcel_id_box))

			summary_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.valueSummBox table tbody')))

			owner = browser.execute_script('return arguments[0].children[0].children[1].innerText', summary_box)
			address = browser.execute_script('return arguments[0].children[1].children[1].innerText', summary_box)
			acreage = browser.execute_script('return arguments[0].children[2].children[1].innerText', summary_box)
			square_footage = browser.execute_script('return arguments[0].children[3].children[1].innerText', summary_box)
			property_type = browser.execute_script('return arguments[0].children[4].children[1].innerText', summary_box)
			tax_district = browser.execute_script('return arguments[0].children[5].children[1].innerText', summary_box)
			land_value = browser.execute_script('return arguments[0].children[6].children[1].innerText', summary_box)
			building_value = browser.execute_script('return arguments[0].children[7].children[1].innerText', summary_box)
			market_value = browser.execute_script('return arguments[0].children[8].children[1].innerText', summary_box)
		except Exception as err:
			print(err, 'failed summary scrape')

		central_ac = ''
		heating = ''
		owner_occupied = ''
		total_rooms = ''
		beds = ''
		baths = ''
		three_fourths_baths = ''
		half_baths = ''
		kitchens = ''
		fire_places = ''
		year_built = ''
		percent_complete = ''
		main_floor_area = ''
		above_ground_area = ''
		basement_area = ''
		finished_basement_area = ''
		above_basement_area = ''

		try:
			residence_record = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#residencetable')))
			
			central_ac = browser.execute_script('return arguments[0].children[1].children[0].children[0].children[4].children[0].innerText', residence_record)
			heating = browser.execute_script('return arguments[0].children[1].children[0].children[0].children[5].children[0].innerText', residence_record)
			owner_occupied = browser.execute_script('return arguments[0].children[1].children[0].children[0].children[6].children[0].innerText', residence_record)
			total_rooms = browser.execute_script('return arguments[0].children[1].children[0].children[0].children[8].children[0].innerText', residence_record)
			beds = browser.execute_script('return arguments[0].children[1].children[0].children[0].children[9].children[0].innerText', residence_record)

			baths = browser.execute_script('return arguments[0].children[1].children[0].children[1].children[0].children[0].innerText', residence_record)
			three_fourths_baths = browser.execute_script('return arguments[0].children[1].children[0].children[1].children[4].children[0].innerText', residence_record)
			half_baths = browser.execute_script('return arguments[0].children[1].children[0].children[1].children[2].children[0].innerText', residence_record)
			kitchens = browser.execute_script('return arguments[0].children[1].children[0].children[1].children[3].children[0].innerText', residence_record)
			fire_places = browser.execute_script('return arguments[0].children[1].children[0].children[1].children[4].children[0].innerText', residence_record)
			year_built = browser.execute_script('return arguments[0].children[1].children[0].children[1].children[5].children[0].innerText', residence_record)

			percent_complete = browser.execute_script('return arguments[0].children[1].children[0].children[2].children[9].children[0].innerText', residence_record)

			main_floor_area = browser.execute_script('return arguments[0].children[1].children[0].children[3].children[0].children[0].innerText', residence_record)
			above_ground_area = browser.execute_script('return arguments[0].children[1].children[0].children[3].children[3].children[0].innerText', residence_record)
			basement_area = browser.execute_script('return arguments[0].children[1].children[0].children[3].children[4].children[0].innerText', residence_record)
			finished_basement_area = browser.execute_script('return arguments[0].children[1].children[0].children[3].children[5].children[0].innerText', residence_record)
			above_basement_area = browser.execute_script('return arguments[0].children[1].children[1].children[0].innerText', residence_record)
		except Exception as err:
			print(err, 'failed residence record')

		scrape_info = dict(
			error=False,
			county='Salt Lake',
			parcel_id=parcel_id.strip(),
			url=browser.current_url.strip(),
			owner=owner.strip(),
			address=address.strip(),
			acreage=acreage.strip(),
			square_footage=square_footage.strip(),
			property_type=property_type.strip(),
			tax_district=tax_district.strip(),
			land_value=land_value.strip(),
			building_value=building_value.strip(),
			market_value=market_value.strip(),
			central_ac=central_ac.strip(),
			heating=heating.strip(),
			owner_occupied=owner_occupied.strip(),
			total_rooms=total_rooms.strip(),
			beds=beds.strip(),
			baths=baths.strip(),
			three_fourths_baths=three_fourths_baths.strip(),
			half_baths=half_baths.strip(),
			kitchens=kitchens.strip(),
			fire_places=fire_places.strip(),
			year_built=year_built.strip(),
			percent_complete=percent_complete.strip(),
			main_floor_area=main_floor_area.strip(),
			above_ground_area=above_ground_area.strip(),
			basement_area=basement_area.strip(),
			finished_basement_area=finished_basement_area.strip()
		)

		return scrape_info
	except Exception as err:
		return {
			'error': True
		}

# info = scrapeSalt('2451', 'e ellisonwoods ave')
# print(info)

# info2 = scrapeSalt('4068', 'S 3200 W')
# print(info2)

# info3 = scrapeSalt('9061', 's greenhills dr')
# print(info3)

# info4 = scrapeSalt('241', 'n vine st # 701e')
# print(info4)

# info5 = scrapeSalt('5908', 's 5625 w')
# print(info5)
