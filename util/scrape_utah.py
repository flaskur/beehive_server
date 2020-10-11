from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains

url = 'http://www.utahcounty.gov/LandRecords/AddressSearchForm.asp'

address = 'n main'.lower()

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get(url)

house_num_field = browser.find_element_by_css_selector('input#av_house')
browser.execute_script("arguments[0].value = '612'", house_num_field)

# all_records_radio = browser.find_element_by_css_selector('input#av_valid_2')
# ActionChains(browser).click(all_records_radio).perform()

search_button = browser.find_element_by_css_selector('input[name="Submit"]')
ActionChains(browser).click(search_button).perform()

rows = browser.find_elements_by_css_selector('table table tbody tr')

print(browser) # is this a web element type?
print(len(rows))

for index, row in enumerate(rows):
	if index < 1 or index == len(rows) - 1:
		print('skipping', index)
		continue

	row_address = browser.execute_script('return arguments[0].children[1].innerText', row)

	if (address in row_address.lower()):
		print(address, 'FOUND IN', row_address)
		

		row_link = browser.execute_script('return arguments[0].children[0].children[0]', row)
		print(row_link.get_attribute('href'))
		# ActionChains(browser).click(row_link).perform()
		browser.get(row_link.get_attribute('href'))

		break

		

	# row_link = browser.execute_script('return arguments[0].children[0].children[0]', row)
	# print(index, row_link.get_attribute('href'))

	
	# print(browser.execute_script('return arguments[0].children', row))
	# print(browser.execute_script('return arguments[0].children[0]', row).get_attribute('innerText'))
	
	# print(row, row.get_attribute('innerHTML'))
	# row_link = row.find_element_by_css_selector('td a') # problem is that it needs to be called from the browser
	# print(row_link.get_attribute('innerText'))
	# row_address = row.find_element_by_css_selector('td:nth-child(2)')
	# print(row_address.get_attribute('innerText'))


table = browser.find_element_by_css_selector('table table tbody')
serial_link = browser.execute_script('return arguments[0].children[1].children[0].children[0]', table)
print(serial_link.get_attribute('href'))
browser.get(serial_link.get_attribute('href'))
print(browser.current_url)