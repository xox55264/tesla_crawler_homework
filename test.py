from selenium import webdriver
import time

def click_element(button_xpath, wait=10):
    retry_counter = 0
    while retry_counter < wait:
        try:
            element = driver.find_element_by_xpath(button_xpath)
            element.click()
            retry_counter = wait
        except:
            retry_counter += 1
            time.sleep(1)

def type_input(input_xpath, input, wait=10):
    retry_counter = 0
    while retry_counter < wait:
        try:
            element = driver.find_element_by_xpath(input_xpath)
            element.send_keys(input)
            retry_counter = wait
        except:
            retry_counter += 1
            time.sleep(1)

def storge_html(url, html):
    file = open(url, mode='w')
    file.write(html)
    file.close()
###
target_car = ['Model 3', 'Model X', 'Model Y']

###
driver = webdriver.Chrome('./chromedriver')
driver.get('https://epc.tesla.com/#/login')
click_element('/html/body/div/div/div/div[2]/div[1]/div/div/form/div/button')

type_input('//*[@id="form-input-identity"]', 'qirui.lan@dataenlighten.com')
click_element('//*[@id="form-submit-continue"]')
type_input('//*[@id="form-input-credential"]', '1qaz2wsx')
click_element('//*[@id="form-submit-continue"]')




for car in target_car:
    print(car)
click_element(f'//td[contains(text(), "Model 3}")]/..//button', 20)
# driver.get('https://epc.tesla.com/#/catalogs')
for sub_group_element in driver.find_elements_by_xpath('//a[contains(@href,"#/categories/")]'):
    sub_group = sub_group_element.get_attribute('href')
    print(sub_group)
    driver.get(sub_group_element.get_attribute('href'))
    for section in driver.find_elements_by_xpath('//a[contains(@href,"#/systemGroups/")]'):
        url = section.get_attribute('href')
        driver.get(section.get_attribute('href'))
        storge_html(url, driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML"))


#driver.close()