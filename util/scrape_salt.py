from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrapeSalt(house_num, street_name):
	address = f'{house_num} {street_name}'.lower()

	options = Options()
	options.headless = True
	browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options) # headless mode
	# browser = webdriver.Chrome(ChromeDriverManager().install()) # opens browser

	# navigate to start webpage --> avoids iframe
	url = 'https://slco.org/assessor/new/searchiframe.cfm'
	browser.get(url)

	# set input house num field
	house_num_field = browser.find_element_by_css_selector('input[name="street_Num"')
	browser.execute_script('arguments[0].value = arguments[1]', house_num_field, house_num)

	# set input street name field
	street_name_field = browser.find_element_by_css_selector('input[name="street_name"')
	browser.execute_script('arguments[0].value = arguments[1]', street_name_field, street_name)

	# press submit button
	submit_button = browser.find_element_by_css_selector('input#Submit')
	browser.execute_script('arguments[0].click()', submit_button)

	# VALIDATE NONZERO SEARCH RESULTS

	# access address rows
	wait = WebDriverWait(browser, 20) # will timeout on 20 seconds of inactivity
	results_white = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsWhite')))
	results_grey = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsGrey')))

	# iterate through white rows, if address matches, immediately move to new url
	found_count = 0
	for result in results_white:
		result_address = browser.execute_script('return arguments[0].children[0].children[2].children[0].children[0].innerText', result)

		if address in result_address.lower():
			source = browser.execute_script('return arguments[0].children[0].getAttribute("onclick")', result)
			new_url = 'https://slco.org/assessor/new/' + source.split("'")[1]
			found_count += 1

			browser.get(new_url)
			break

	# only check grey rows if white rows failed
	if found_count < 1:
		for result in results_grey:
			result_address = browser.execute_script('return arguments[0].children[0].children[2].children[0].children[0].innerText', result)

			if address in result_address.lower():
				source = browser.execute_script('return arguments[0].children[0].getAttribute("onclick")', result)
				new_url = 'https://slco.org/assessor/new/' + source.split("'")[1]
				found_count += 1

				browser.get(new_url)
				break

	# no address match, return error
	if found_count < 1:
		return {
			'error': True
		}


	# scrape summary box
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

	print()
	print('OWNER:', owner)
	print('ADDRESS:', address)
	print('TOTAL ACREAGE:', total_acreage)
	print('ABOVE GRADE SQFT:', above_grade_sqft)
	print('PROPERTY TYPE:', property_type)
	print('TAX DISTRICT:', above_grade_sqft)
	print('LAND VALUE:', land_value)
	print('BUILDING VALUE:', building_value)
	print('MARKET VALUE:', market_value)

	# scrape value history
	value_history = browser.find_element_by_css_selector('div#valuehistory table tbody')

	# convert this into an array of hash maps to get all years
	last_history = {}
	last_history['year'] = browser.execute_script('return arguments[0].children[0].children[0].innerText', value_history)
	last_history['land_value'] = browser.execute_script('return arguments[0].children[0].children[2].innerText', value_history)
	last_history['building_value'] = browser.execute_script('return arguments[0].children[0].children[3].innerText', value_history)
	last_history['market_value'] = browser.execute_script('return arguments[0].children[0].children[4].innerText', value_history)

	second_last_history = {}
	second_last_history['year'] = browser.execute_script('return arguments[0].children[1].children[0].innerText', value_history)
	second_last_history['land_value'] = browser.execute_script('return arguments[0].children[1].children[2].innerText', value_history)
	second_last_history['building_value'] = browser.execute_script('return arguments[0].children[1].children[3].innerText', value_history)
	second_last_history['market_value'] = browser.execute_script('return arguments[0].children[1].children[4].innerText', value_history)

	print()
	print(last_history, second_last_history)
	print()

	central_ac = None
	heating = None
	owner_occupied = None
	total_rooms = None
	bedrooms = None
	full_baths = None
	three_quarters_baths = None
	half_baths = None
	num_kitchens = None
	fire_places = None
	year_built = None
	percent_complete = None
	main_floor_area = None
	above_ground_area = None
	basement_area = None
	finished_basement_area = None

	# scrape residence record
	try:
		residence_record = browser.find_element_by_css_selector('div#residencetable')
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
	except Exception as err:
		print('failed to get residence record')
		print(err)

	print('CENTRAL AC:', central_ac)
	print('HEATING:', heating)
	print('OWNER OCCUPIED:', owner_occupied)
	print('TOTAL ROOMS:', total_rooms)
	print('BEDROOMS:', bedrooms)
	print('FULL BATHS:', full_baths)
	print('THREE QUARTERS BATHS:', three_quarters_baths)
	print('HALF BATHS:', half_baths)
	print('NUM KITCHENS:', num_kitchens)
	print('FIRE PLACES:', fire_places)
	print('YEAR BUILT:', year_built)
	print('PERCENT COMPLETE:', percent_complete)
	print('MAIN FLOOR AREA:', main_floor_area)
	print('ABOVE GROUND AREA:', above_ground_area)
	print('BASEMENT AREA:', basement_area)
	print('FINISHED BASEMENT AREA:', finished_basement_area)

	scrape_info = dict(
		error=False,
		url=browser.current_url,
		owner=owner,
		address=address,
		total_acreage=total_acreage,
		above_grade_sqft=above_grade_sqft,
		property_type=property_type,
		tax_district=tax_district,
		land_value=land_value,
		building_value=building_value,
		market_value=market_value,
		central_ac=central_ac,
		heating=heating,
		owner_occupied=owner_occupied,
		total_rooms=total_rooms,
		bedrooms=bedrooms,
		full_baths=full_baths,
		three_quarters_baths=three_quarters_baths,
		half_baths=half_baths,
		num_kitchens=num_kitchens,
		fire_places=fire_places,
		year_built=year_built,
		percent_complete=percent_complete,
		main_floor_area=main_floor_area,
		above_ground_area=above_ground_area,
		basement_area=basement_area,
		finished_basement_area=finished_basement_area
	)

	return scrape_info

# info = scrapeSalt('2451', 'e ellisonwoods ave')

# print(info)
# print(info['url'])

info2 = scrapeSalt('4068', 'S 3200 W') # I expect residence record to fail, ignores and returns as None

print(info2)
print(info2['url'])

# NEED TO VALIDATE CSS SELECTIONS
