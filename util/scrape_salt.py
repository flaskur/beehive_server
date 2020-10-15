from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains

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

account_rows = browser.find_elements_by_css_selector('table tbody tr')

num_results = browser.find_element_by_css_selector('div#resultsDiv div strong') # breaks here for some reason, query selection isn't working
print('num results is', num_results.innerText)

if num_results == '0':
	print('there are zero results, shoudl return an empty dict with no info or an error')

# for row, index in account_rows:
# 	# skip every even index since top is header and each table row has an associated image container 

# you could either access row by num based on num_results, or using the resultsWhite and resultsGrey classes
for i in range(1, int(num_results) + 1):
	# should be a try except case...
	id = 'resultBlock' + str(i)
	detail_type = 'detailType' + str(i)
	print('id is', id)
	row = browser.find_element_by_css_selector(id)

	query_arg = f'return arguments[0].querySelector("{detail_type}.innerText")'
	print('query is', query_arg)
	address_name = browser.execute_script(query_arg)

	print('address name', address_name)