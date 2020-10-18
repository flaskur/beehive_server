from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

address = '2451 E ELLISONWOODS AVE'.lower()

url = 'https://slco.org/assessor/new/searchiframe.cfm'

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get(url)

house_num_field = browser.find_element_by_css_selector('input[name="street_Num"')
browser.execute_script('arguments[0].value = arguments[1]', house_num_field, '2451')

street_name_field = browser.find_element_by_css_selector('input[name="street_name"')
browser.execute_script('arguments[0].value = arguments[1]', street_name_field, 'Ellisonwoods Ave')

submit_button = browser.find_element_by_css_selector('input#Submit')
browser.execute_script('arguments[0].click()', submit_button)

# should validate if there are nonzero search results here



wait = WebDriverWait(browser, 20)

results_white = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsWhite')))
results_grey = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsGrey')))

found_count = 0

for result in results_white:
	result_address = browser.execute_script('return arguments[0].children[0].children[2].children[0].children[0].innerText', result)
	print('result address', result_address)
	if address in result_address.lower():
		print('found match', address, result_address)

		# source = browser.execute_script('return arguments[0].children[0].onclick', result)
		source = browser.execute_script('return arguments[0].children[0].getAttribute("onclick")', result)
		print('source is', source)
		new_url = 'https://slco.org/assessor/new/' + source.split("'")[1]
		print(new_url)
		found_count += 1

		browser.get(new_url)
		break

if found_count < 1:
	for result in results_grey:
		result_address = browser.execute_script('return arguments[0].children[0].children[2].children[0].children[0].innerText', result)
		print('result address', result_address)
		if address in result_address.lower():
			print('found match', address, result_address)

			# source = result.get_attribute('onclick')
			source = browser.execute_script('return arguments[0].children[0].getAttribute("onclick")', result)
			new_url = 'https://slco.org/assessor/new/' + source.split("'")[1]
			print(new_url)
			found_count += 1

			browser.get(new_url)
			break

if found_count < 1:
	print('no found address')

summary_box = browser.find_element_by_css_selector('div.valueSummBox table tbody')

owner = browser.execute_script('return arguments[0].children[0].children[1].innerText', summary_box)
address = browser.execute_script('return arguments[0].children[1].children[1].innerText', summary_box)
total_acreage = browser.execute_script('return arguments[0].children[2].children[1].innerText', summary_box)
above_grade_sqft = browser.execute_script('return arguments[0].children[3].children[1].innerText', summary_box)
property_type = browser.execute_script('return arguments[0].children[4].children[1].innerText', summary_box)
tax_district = browser.execute_script('return arguments[0].children[5].children[1].innerText', summary_box)
land_value = browser.execute_script('return arguments[0].children[6].children[1].innerText', summary_box)
building_value = browser.execute_script('return arguments[0].children[7].children[1].innerText', summary_box)
market_value = browser.execute_script('return arguments[0].children[8].children[1].innerText', summary_box)

print(owner, address, total_acreage, above_grade_sqft, property_type, tax_district, land_value, building_value, market_value)

value_history = browser.find_element_by_css_selector('div#valuehistory table tbody')

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

print(last_history, second_last_history)

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

print(central_ac, heating, owner_occupied, total_rooms, bedrooms, full_baths, three_quarters_baths, half_baths, num_kitchens, fire_places, year_built, percent_complete, main_floor_area, above_ground_area, basement_area, finished_basement_area)

# for link in links_white:
# 	link_address = browser.execute_script('return arguments[0].innerText', link)
# 	print(link_address)
# 	if address in link_address.lower():
# 		print('found match', address, link_address)
# 		found_count += 1
# 		ActionChains(browser).click(link).perform()

# for link in links_grey:
# 	link_address = browser.execute_script('return arguments[0].innerText', link)
# 	print(link_address)
# 	if address in link_address.lower():
# 		print('found match', address, link_address)
# 		found_count += 1
# 		ActionChains(browser).click(link).perform()

# # so it checks every one and there might be duplicates, but it technically should link to the last one
# if found_count < 1:
# 	print('found nothing')
# 	# should return error here


# # you might want to do browser get url instead
# detail = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div#detailDiv')))
# print(detail.innerText)

# wait = WebDriverWait(browser, 10)
# results_white = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsWhite')))
# results_grey = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsGrey')))
# # time.sleep(4)


# # results_white = browser.find_elements_by_css_selector('tr.resultsWhite div div a')
# # results_grey = browser.find_element_by_css_selector('tr.resultsGrey div div a')

# for result in results_white:
# 	result_address = browser.execute_script('return arguments[0].children[0].children[2].children[0].children[0].innerText', result)
# 	print('result address', result_address)
# 	if address in result_address.lower():
# 		print('found a match', address, result_address)


# for result in results_grey:
# 	result_address = browser.execute_script('return arguments[0].children[0].children[2].children[0].children[0].innerText', result)
# 	print('result address', result_address)
# 	if address in result_address.lower():
# 		print('found a match', address, result_address)

# click on a link goes to new tab, might be an issue, also means we can shorten the css selector

# account_rows = browser.find_elements_by_css_selector('table tbody tr')

# num_results = browser.find_element_by_css_selector('div#resultsDiv div strong') # breaks here for some reason, query selection isn't working
# print('num results is', num_results.innerText)

# if num_results == '0':
# 	print('there are zero results, shoudl return an empty dict with no info or an error')

# # for row, index in account_rows:
# # 	# skip every even index since top is header and each table row has an associated image container 

# # you could either access row by num based on num_results, or using the resultsWhite and resultsGrey classes
# for i in range(1, int(num_results) + 1):
# 	# should be a try except case...
# 	id = 'resultBlock' + str(i)
# 	detail_type = 'detailType' + str(i)
# 	print('id is', id)
# 	row = browser.find_element_by_css_selector(id)

# 	query_arg = f'return arguments[0].querySelector("{detail_type}.innerText")'
# 	print('query is', query_arg)
# 	address_name = browser.execute_script(query_arg)

# 	print('address name', address_name)