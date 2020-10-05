from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains

# def scrapeTooele(street_num, street_name):

url = 'https://erecording.tooeleco.org/eaglesoftware/web/login.jsp'

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get(url)

enter_button = browser.find_element_by_css_selector('input[name="submit"]')
print(enter_button.get_attribute('value'))
ActionChains(browser).click(enter_button).perform()

accept_button = browser.find_element_by_css_selector('input[name="accept"]')
print(accept_button.get_attribute('value'))
ActionChains(browser).click(accept_button).perform()

house_num_field = browser.find_element_by_css_selector('#SitusIDHouseNumber')
print(house_num_field.get_attribute('name'))
# browser.execute_script("arguments[0].value = arguments[1]", house_num_field, street_num)
browser.execute_script("arguments[0].value = '325'", house_num_field)

street_name_field = browser.find_element_by_css_selector('#SitusIDStreetName')
print(street_name_field.get_attribute('name'))
browser.execute_script("arguments[0].value = 'valley view dr'", street_name_field)

search_button = browser.find_element_by_css_selector('input[value="Search"]')
print(street_name_field.get_attribute('value'))
ActionChains(browser).click(search_button).perform()

# HERE YOU SHOULD CHECK IF ADDRESS IS VALID BY CHECKING IF HTML ELEMENT EXISTS
account_row = browser.find_element_by_css_selector('td.clickable')
print(account_row.get_attribute('innerHTML'))
ActionChains(browser).click(account_row).perform()

# If you put this logic in a function it quits and crashes chrome for some reason.
# This is actually by design, which is better and won't matter since you'll have extracted and returned the information by then.



# scrapeTooele('325', 'valley view dr')

# header_search_field = driver.find_element_by_css_selector('#header_searchfield')

# # header_search_field.set_attribute('value', 'banana')

# print(header_search_field.get_attribute('value'))

# driver.execute_script("arguments[0].value = 'banana'", header_search_field)

# street_num_field = driver.find_element_by_css_selector("td input.search-box")

# print(street_num_field)

# driver.execute_script("arguments[0].value = '123'", street_num_field)

