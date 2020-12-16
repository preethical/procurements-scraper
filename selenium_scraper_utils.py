'Class for Selenium Scrapping utility functions'

import logging
from logging.config import fileConfig
from lxml import etree
import os
import re
import requests
from requests.adapters import HTTPAdapter
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import shutil
from urllib3.util import Retry

DEFAULT_XPATH = ".//text()"
MAX_URL_RETRIES = 25
SAMPLE_URL = "https://www.civicdatalab.in/"
TEXT_DOC_XPATH = "//text()"
SLEEP_TIME = 60
MAX_RELOADS = 3

class SeleniumScrappingUtils(object):
    def __init__(self):
        '''Initializes session for scrapping utils
        '''
        self.retry_status_codes = [404,500,502,503,504] 
        headlessOpt = Options()
        headlessOpt.headless = True
        self.driver = webdriver.Firefox(options=headlessOpt) 
        self.driver.get(SAMPLE_URL)

    def get_page_from_url(self, url):
        '''Fetches URL and return its textual content, in case of error returns empty text
        '''
        page_text = ''
        self.driver.get(url)
        time.sleep(1)
        page_text = self.driver.page_source
        return page_text

    def get_page_dom(self, url=None):
        '''Returns dom tree of the driver's page source
        '''
        dom_tree = None
        if url:
            page_text = self.get_page_from_url(url)
        else:
            time.sleep(1)
            page_text = self.driver.page_source
        if page_text:
            dom_tree = etree.HTML(page_text)
        return dom_tree

    def get_page_element(self, xpath=None):
        ''' Get page element by xpath
        '''
        page_element = None
        reload_attempts = 0
        while not page_element and reload_attempts < MAX_RELOADS:
            try:
                page_element = WebDriverWait(self.driver, SLEEP_TIME).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
            except NoSuchElementException as error_message:
                print(error_message)
            except Exception as error_message:
                print(error_message)
            if not page_element:
                self.driver.refresh()
            reload_attempts += 1 
        return page_element
    
    def select_element(self, select_element, text=None):
        select = Select(select_element)
        select.select_by_visible_text(text)
