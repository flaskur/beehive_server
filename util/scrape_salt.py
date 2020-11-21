from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unicodedata

def scrapeSalt(house_num, street_name):
	try:
		address = f'{house_num} {street_name}'.lower()

		options = Options()
		options.headless = True
		browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # headless mode
		# browser = webdriver.Chrome(ChromeDriverManager().install()) # opens browser

		url = 'https://slco.org/assessor/new/searchiframe.cfm'
		browser.get(url)

		house_num_field = browser.find_element_by_css_selector('input[name="street_Num"]')
		browser.execute_script('arguments[0].value = arguments[1]', house_num_field, house_num)

		street_name_field = browser.find_element_by_css_selector('input[name="street_name"]')
		browser.execute_script('arguments[0].value = arguments[1]', street_name_field, street_name)

		submit_button = browser.find_element_by_css_selector('input#Submit')
		browser.execute_script('arguments[0].click()', submit_button)

		wait = WebDriverWait(browser, 5)

		results_white = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsWhite')))

		new_urls = []

		# iterate through white rows, if address matches, immediately move to new url
		found_count = 0
		for result in results_white:
			result_address = browser.execute_script('return arguments[0].children[0].children[2].children[0].children[0].innerText', result)

			if address in result_address.lower():
				source = browser.execute_script('return arguments[0].children[0].getAttribute("onclick")', result)
				new_url = 'https://slco.org/assessor/new/' + source.split("'")[1]
				found_count += 1
				new_urls.append(new_url)

				# browser.get(new_url)
				break

		results_grey = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsGrey')))

		for result in results_grey:
			result_address = browser.execute_script('return arguments[0].children[0].children[2].children[0].children[0].innerText', result)

			if address in result_address.lower():
				source = browser.execute_script('return arguments[0].children[0].getAttribute("onclick")', result)
				new_url = 'https://slco.org/assessor/new/' + source.split("'")[1]
				found_count += 1
				new_urls.append(new_url)

				# browser.get(new_url)
				break

		# no address match, return error
		if found_count < 1:
			return {
				'error': True
			}

		print(new_urls)

		# for now assume we take the last url?
		browser.get(new_urls[-1])

		parcel_id_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#parcelFieldNames div div strong')))
		parcel_id = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].innerText', parcel_id_box))

		summary_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.valueSummBox table tbody')))

		owner = browser.execute_script('return arguments[0].children[0].children[1].innerText', summary_box)
		address = browser.execute_script('return arguments[0].children[1].children[1].innerText', summary_box)
		total_acreage = browser.execute_script('return arguments[0].children[2].children[1].innerText', summary_box)
		above_grade_sqft = browser.execute_script('return arguments[0].children[3].children[1].innerText', summary_box)
		property_type = browser.execute_script('return arguments[0].children[4].children[1].innerText', summary_box)
		tax_district = browser.execute_script('return arguments[0].children[5].children[1].innerText', summary_box)
		land_value = browser.execute_script('return arguments[0].children[6].children[1].innerText', summary_box)
		building_value = browser.execute_script('return arguments[0].children[7].children[1].innerText', summary_box)
		market_value = browser.execute_script('return arguments[0].children[8].children[1].innerText', summary_box)

		val_history = [] # array of maps

		# scrape value history
		try:
			value_history = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#valuehistory table tbody')))

			i = 0
			# iterate for last 5 assumption, or iterate until failure 
			while i < 5:
				history = {}
				history['year'] = browser.execute_script('return arguments[0].children[arguments[1]].children[0].innerText', value_history, i).strip()
				history['land_value'] = browser.execute_script('return arguments[0].children[arguments[1]].children[2].innerText', value_history, i).strip()
				history['building_value'] = browser.execute_script('return arguments[0].children[arguments[1]].children[3].innerText', value_history, i).strip()
				history['market_value'] = browser.execute_script('return arguments[0].children[arguments[1]].children[4].innerText', value_history, i).strip()

				val_history.append(history)
				i += 1
		except Exception as err:
			print(err, 'failed value history')

			
		central_ac = ''
		heating = ''
		owner_occupied = ''
		total_rooms = ''
		bedrooms = ''
		full_baths = ''
		three_quarters_baths = ''
		half_baths = ''
		num_kitchens = ''
		fire_places = ''
		year_built = ''
		percent_complete = ''
		main_floor_area = ''
		above_ground_area = ''
		basement_area = ''
		finished_basement_area = ''
		above_basement_area = ''

		# condos have different residence record that doesn't work for this check
		try:
			residence_record = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#residencetable')))
			print('RESIDENCE RECORD FOUND')
			
			central_ac = browser.execute_script('return arguments[0].children[1].children[0].children[0].children[4].children[0].innerText', residence_record)
			heating = browser.execute_script('return arguments[0].children[1].children[0].children[0].children[5].children[0].innerText', residence_record)
			owner_occupied = browser.execute_script('return arguments[0].children[1].children[0].children[0].children[6].children[0].innerText', residence_record)
			total_rooms = browser.execute_script('return arguments[0].children[1].children[0].children[0].children[8].children[0].innerText', residence_record)
			bedrooms = browser.execute_script('return arguments[0].children[1].children[0].children[0].children[9].children[0].innerText', residence_record)

			full_baths = browser.execute_script('return arguments[0].children[1].children[0].children[1].children[0].children[0].innerText', residence_record)
			three_quarters_baths = browser.execute_script('return arguments[0].children[1].children[0].children[1].children[4].children[0].innerText', residence_record)
			half_baths = browser.execute_script('return arguments[0].children[1].children[0].children[1].children[2].children[0].innerText', residence_record)
			num_kitchens = browser.execute_script('return arguments[0].children[1].children[0].children[1].children[3].children[0].innerText', residence_record)
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


		# html code is unique depending on whether or not there is 1 or greater than 1 detached structure
		det_structures = []
		try:
			detached_structures = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#detachedTable table tbody')))

			i = 1
			# we expect an error, but we still need to build structure hash map
			while True:
				structure = {}

				# weird \xa0 append
				structure['name'] = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[0].children[arguments[1]].innerText', detached_structures, i)).strip()
				structure['measure1'] = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[4].children[arguments[1]].innerText', detached_structures, i)).strip()
				structure['measure2'] = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[5].children[arguments[1]].innerText', detached_structures, i)).strip()
				structure['actual_year_built'] = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[7].children[arguments[1]].innerText', detached_structures, i)).strip()
				structure['replacement_cost_new'] = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[11].children[arguments[1]].innerText', detached_structures, i)).strip()
				
				det_structures.append(structure)
				i += 1
		except Exception as err:
			print('FINISHED ALL DET STRUCTURES OR...')
			print('NOT MULTI DETACHED STRUCTURE TABLE')
			print(err)

			try:
				detached_structures = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#detachedTable div.details')))

				structure = {}

				structure['name'] = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[1].children[0].children[0].children[0].innerText', detached_structures)).strip()
				structure['measure1'] = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[1].children[4].children[0].children[0].innerText', detached_structures)).strip()
				structure['measure2'] = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[1].children[5].children[0].children[0].innerText', detached_structures)).strip()
				structure['actual_year_built'] = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[2].children[1].children[0].children[0].innerText', detached_structures)).strip()
				structure['replacement_cost_new'] = unicodedata.normalize('NFKD', browser.execute_script('return arguments[0].children[3].children[0].children[0].children[0].innerText', detached_structures)).strip()

				det_structures.append(structure)
			except Exception as err:
				print('ACTUALLY NO DETACHED STRUCTURES')
				print(err)


		scrape_info = dict(
			error=False,
			parcel_id=parcel_id.strip(),
			url=browser.current_url.strip(),
			owner=owner.strip(),
			address=address.strip(),
			total_acreage=total_acreage.strip(),
			above_grade_sqft=above_grade_sqft.strip(),
			property_type=property_type.strip(),
			tax_district=tax_district.strip(),
			land_value=land_value.strip(),
			building_value=building_value.strip(),
			market_value=market_value.strip(),
			val_history=val_history,
			central_ac=central_ac.strip(),
			heating=heating.strip(),
			owner_occupied=owner_occupied.strip(),
			total_rooms=total_rooms.strip(),
			bedrooms=bedrooms.strip(),
			full_baths=full_baths.strip(),
			three_quarters_baths=three_quarters_baths.strip(),
			half_baths=half_baths.strip(),
			num_kitchens=num_kitchens.strip(),
			fire_places=fire_places.strip(),
			year_built=year_built.strip(),
			percent_complete=percent_complete.strip(),
			main_floor_area=main_floor_area.strip(),
			above_ground_area=above_ground_area.strip(),
			basement_area=basement_area.strip(),
			finished_basement_area=finished_basement_area.strip(),
			det_structures=det_structures
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

# need to handle duplicate correct addresses, allow user to select eventually