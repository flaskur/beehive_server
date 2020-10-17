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



wait = WebDriverWait(browser, 10)
links_white = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsWhite td div div a')))
links_grey = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'tr.resultsGrey td div div a')))

for link in links_white:
	link_address = browser.execute_script('return arguments[0].innerText', link)
	print(link_address)
	if address in link_address.lower():
		print('found match', address, link_address)
		ActionChains(browser).click(link).perform()

for link in links_grey:
	link_address = browser.execute_script('return arguments[0].innerText', link)
	print(link_address)
	if address in link_address.lower():
		print('found match', address, link_address)
		ActionChains(browser).click(link).perform()



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