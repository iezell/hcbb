import scrapy
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidSessionIdException
from urllib.parse import urlencode

class mriGreen(scrapy.Spider):
    name = "mriGreen"

    searchTerm = "MRI"
    searchZipCode = "37201"

    allowed_domains = ['healthcarebluebook.com']
    start_urls = ['https://www.healthcarebluebook.com/ui/consumerfront']

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--incognito')
        # options.add_argument('--headless')

        self.driver = webdriver.Chrome(chrome_options=options)

    def parse(self, response):
        self.driver.get(response.url)

        delay = 10 # seconds
        timerDelay = 30
        try:
            #/ui/consumerfront
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, 'ibSearch')))
            zipbox = self.driver.find_element_by_id("tbZipCode2")
            zipbox.send_keys(self.searchZipCode)
            sbox = self.driver.find_element_by_id("ibSearch")
            sbox.send_keys(self.searchTerm)
            submit = self.driver.find_element_by_id("ibSubmitSearch")
            submit.click()

            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'select-user-type')))
            time.sleep(timerDelay)
            self.driver.find_elements_by_xpath("//*[contains(text(), 'All other visitors')]")[0].click()
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'service-name')))

            soupedBody = BeautifulSoup(self.driver.page_source, "lxml")
            servicesDiv = soupedBody.find_all('div', class_='service-name')

            cur_win = self.driver.current_window_handle

            serviceLinks = []
            time.sleep(timerDelay)
            for service in servicesDiv:
                print(service.getText())

                # self.driver.execute_script("window.open('');")
                # self.driver.switch_to.window(self.driver.window_handles[1])

                self.driver.find_element_by_link_text(service.getText()).send_keys('\n')
                WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'provider-list')))

                soupedProcedure = BeautifulSoup(self.driver.page_source, "lxml")
                locationDiv = soupedProcedure.find_all('div', {"class" : lambda L: L and L.startswith('detail-item facility-id-')})

                for elements in locationDiv:
                    procedureName = elements.find('div', class_='facility-name')
                    time.sleep(timerDelay)
                    self.driver.find_element_by_link_text(procedureName.find('a').contents[0]).send_keys('\n')
                    WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'facility-info-container')))
                    time.sleep(timerDelay)
                    self.driver.execute_script("window.history.go(-1)")
                    time.sleep(timerDelay)
                    WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'facility-name')))

                # self.driver.switch_to.window(self.driver.window_handles[0])
                time.sleep(timerDelay)
                self.driver.execute_script("window.history.go(-1)")
                time.sleep(timerDelay)
                self.driver.execute_script("window.history.go(-1)")

                WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'service-name')))

        except TimeoutException:
            print("Loading Timeout")

        self.driver.close()
