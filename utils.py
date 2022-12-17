from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import os

class Parse(object):
    def __init__(self):
        self.info_xpath = {'modle': '/html/body/div/div/div[1]/div/breadcrumbs/ol/li[1]/a',
                           'group': '/html/body/div/div/div[1]/div/breadcrumbs/ol/li[2]/a',
                           'sub_group': '/html/body/div/div/div[1]/div/breadcrumbs/ol/li[3]/a',
                           'section': '/html/body/div/div/div[1]/div/breadcrumbs/ol/li[4]/span'}

        self.table_xpath = {'part': '//*[@id="container"]/div/table/tbody/tr/td[2]/div/div[2]/strong',
                            'part_number': '//*[@id="container"]/div/table/tbody/tr/td[4]',
                            'sales_restraction': '//*[@id="container"]/div/table/tbody/tr/td[5]',
                            'unit_price': '//*[@id="container"]/div/table/tbody/tr/td[6]',
                            'quantity': '//*[@id="container"]/div/table/tbody/tr/td[7]'}
        self.columns = ['modle', 'group', 'sub_group', 'section', 'part', 'part_number', 'sales_restraction',
                        'unit_price', 'quantity']
        self.csv_file = 'output.csv'

    def dict_transform(self, data):
        transformed_data = []
        length = len(data['part'])
        for i in range(length):
            # print(i)
            transformed_data.append({'modle': data['modle'],
                                     'group': data['group'],
                                     'sub_group': data['sub_group'],
                                     'section': data['section'],
                                     'part': data['part'][i],
                                     'part_number': data['part_number'][i],
                                     'sales_restraction': data['sales_restraction'][i],
                                     'unit_price': data['unit_price'][i],
                                     'quantity': data['quantity'][i]})
        return transformed_data


    def storge_data(self, data):
        try:
            with open(self.csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.columns)
                if os.stat(self.csv_file).st_size == 0:
                    writer.writeheader()
                for row in data:
                    writer.writerow(row)
        except IOError:
            print("I/O error")

    def parse_table(self, driver, key, wait=60):
        retry_counter = 0
        while retry_counter < wait:
            try:
                data = []
                for element in driver.find_elements_by_xpath(self.table_xpath[key]):
                    data.append(element.text)
                retry_counter = wait
            except:
                retry_counter += 1
                time.sleep(1)
        return data

    def parse_model_info(self, driver, wait=60):
        data = {}
        for key in self.info_xpath:
            retry_counter = 0
            while retry_counter < wait:
                try:
                    data[key] = driver.find_element_by_xpath(self.info_xpath[key]).text
                    retry_counter = wait
                except:
                    retry_counter += 1
                    time.sleep(1)
        return data

    def parse_data(self, driver):
        data = self.parse_model_info(driver)
        for key in self.table_xpath:
            data[key] = self.parse_table(driver, key)
        transformed_data = self.dict_transform(data)
        self.storge_data(transformed_data)
        print(data['section'])


class Source(object):
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager.install())
        self.parse = Parse()

    def click_element(self, button_xpath, wait=10):
        retry_counter = 0
        while retry_counter < wait:
            try:
                element = self.driver.find_element_by_xpath(button_xpath)
                element.click()
                retry_counter = wait
            except:
                retry_counter += 1
                time.sleep(1)

    def type_input(self, input_xpath, input, wait=10):
        retry_counter = 0
        while retry_counter < wait:
            try:
                element = self.driver.find_element_by_xpath(input_xpath)
                element.send_keys(input)
                retry_counter = wait
            except:
                retry_counter += 1
                time.sleep(1)

    def login(self, account, password):
        self.driver.get('https://epc.tesla.com/#/login')
        time.sleep(2)
        self.click_element('/html/body/div/div/div/div[2]/div[1]/div/div/form/div/button')
        self.type_input('//*[@id="form-input-identity"]', account)
        self.click_element('//*[@id="form-submit-continue"]')
        self.type_input('//*[@id="form-input-credential"]', password)
        self.click_element('//*[@id="form-submit-continue"]')

    def list_category(self):
        self.driver.get('https://epc.tesla.com/#/catalogs')
        time.sleep(2)

    def get_all_elements(self, xpath, wait=10):
        retry_counter = 0
        while retry_counter < wait:
            if self.driver.find_elements_by_xpath(xpath):
                return self.driver.find_elements_by_xpath(xpath)
            else:
                time.sleep(1)
                retry_counter += 1

    def get_sub_group_url(self):
        sub_group_url = []
        for sub_group in self.get_all_elements('//a[contains(@href,"#/categories/")]', 60):
            sub_group_url.append(sub_group.get_attribute('href'))
        return sub_group_url

    def get_section_url(self, sub_group_url):
        section_url = []
        for url in sub_group_url:
            self.driver.get(url)
            time.sleep(2)
            for section in self.get_all_elements('//a[contains(@href,"#/systemGroups/")]', 60):
                section_url.append(section.get_attribute('href'))
        return section_url

    def load_section(self, url, wait=10):
        retry_counter = 0
        is_loaded = True
        self.driver.get(url)
        time.sleep(5)

        while retry_counter < wait:
            try:
                self.driver.find_element_by_xpath('//*[@id="container"]/div/table')
                is_loaded = True
                retry_counter = wait
            except:
                is_loaded = False
                time.sleep(1)
                retry_counter += 1
        return is_loaded

    def start_crawl(self, model):
        self.click_element(f'//td[contains(text(), "{model}")]/..//button', 20)
        sub_group_url = self.get_sub_group_url()
        section_url = self.get_section_url(sub_group_url)
        for url in section_url:
            if self.load_section(url, 20):
                self.parse.parse_data(self.driver)



        # print(section_url)
        # for url in sub_group_url:
        #     self.driver.get(url)
        #     time.sleep(2)
        #     print(url)
            # self.parse.parse_data(self.driver)
        # for sub_group in self.get_all_elements('//a[contains(@href,"#/categories/")]', 60):
            # self.driver.get(sub_group.get_attribute('href'))
            # print(url)
            # for section in self.get_all_elements('//a[contains(@href,"#/systemGroups/")]', 60):
            #     print(section.get_attribute('href'))
                # self.driver.get(section.get_attribute('href'))
                # self.parse.parse_data(self.driver)
