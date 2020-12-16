#!/usr/bin/python3
# -*- coding: utf-8 -*-

'Class for scrapping eProcurement MMP Portal for HP Result of Tenders'

import argparse
import csv
import datetime
from lxml import etree
import logging
from logging.config import fileConfig
import os
import re
from selenium_scraper_utils import SeleniumScrappingUtils
import sys, traceback
import time

OUT_HEADER = ["S.No.", "AOC Date", "e-Published Date", "Title and Ref.No./Tender Id", "State Name"]
BASE_URL = "https://eprocure.gov.in/mmp/resultoftenders"
SLEEP_TIME = 2

class EprocMmpAocHPscraper(SeleniumScrappingUtils):

    def get_tender_results(self, output_file):
        tender_results = []
        csv_writer,out_csv_file = self.get_file_writer(output_file)
        page_dom = self.get_page_dom(url=BASE_URL)
        state_elem = self.get_page_element(xpath='//select[@name="org_name"]')
        #TODO CAUTION
        #self.select_element(state_elem, text="Himachal Pradesh")
        #time.sleep(20) #Enter CAPTCHA
        #submit_button = self.get_page_element(xpath='//input[@value="Search"]')
        #submit_button.click()
        #time.sleep(SLEEP_TIME)
        page_dom = self.get_page_dom() 
        #TODO CAUTION
        url = self.driver.current_url
        url = url + "/page=6750"
        page_dom = self.get_page_dom(url)
        while True:
            tender_records = self.get_tender_records_from_page(page_dom) 
            self.write_tender_details(tender_records, csv_writer)
            print(tender_records)
            time.sleep(SLEEP_TIME)
            previous_button = self.get_page_element(xpath="//a[@class='page_parination' and contains(.,'Previous')]") ##changed this to previous
            if not previous_button:
                break
            previous_button.click()
            time.sleep(SLEEP_TIME)
            page_dom = self.get_page_dom() 
        out_csv_file.close()

    def get_tender_records_from_page(self, page_dom):
        record_list = []
        rows = page_dom.xpath("//div[@id='edit-l-result-teners']/table[@id='table']//tr")
        for row_number in range(len(rows)):
            if row_number == 0:
                continue #Skipping Empty Row
            row = rows[row_number]
            records = row.xpath(".//td//text()")
            records.remove(' ')
            tender_id = records[3].split(" / ")[-1].strip()
            records.append(tender_id)
            
            ##Removing "award of contract details" page
            ##record_link = self.get_page_element(xpath=".//tr[%s]//td[4]/a" % format(row_number+1))
            ##if record_link:
                ##record_link.click()
                ##page_dom = self.get_page_dom()
                ##records_details = self.get_tender_details(page_dom)
                ##records += records_details
                ##back_link = self.get_page_element(xpath="//form[@id='aocfullview-form']//a[1]") 
                ##back_link.click()
            print(records)
            record_list.append(records)
        return record_list

    def get_tender_details(self, page_dom):
        tender_details = page_dom.xpath("//td[@class='td_view_field']//text()")
        return tender_details

    def get_file_writer(self, output_file):
        out_csv_file = open(output_file, "w") #changed this from wb to w
        csv_writer = csv.writer(out_csv_file, delimiter=',')
        csv_writer.writerow(OUT_HEADER)
        return csv_writer, out_csv_file
    
    def write_tender_details(self, tender_records, csv_writer):
        for row in tender_records:
            encoded_row = self.encode_row(row)
            csv_writer.writerow(encoded_row)
        return csv_writer

    def encode_row(self, row):
        encoded_row = []
        for item in row:
            item = item.encode('utf-8')
            encoded_row.append(item)
        return encoded_row

if __name__ == '__main__':
    obj = EprocMmpAocHPscraper()
    obj.get_tender_results("results_all_records_table.csv")
    print("FINISHED SCRAPING.")

