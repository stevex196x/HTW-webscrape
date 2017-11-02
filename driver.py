#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:50:34 2017

The main program that uses Selenium in order to automate the input of zip 
codes into healthytexaswomen.org and scrape its data into a .CSV file

Dependencies:
    Selenium
    BeautifulSoup

@author: steve
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from BeautifulSoup import bs4

import csv
import re
import time

# Hard coded cities in Texas that encompass the entire state within a
# 100 mile radius of each other
# It's a lot faster compared to running a script that iterates through all
# ~2600 zip codes that would hammer the server and process through duplicates

cities = ['Dallas, TX',
          'Austin, TX',
          'Wichita Falls, TX'
          'Abilene, TX',
          'Masterson, TX',
          'Canadian, Tx',
          'Lubbock, TX'
          'Childress, TX',
          'Naples, TX',
          'Weeping Mary, TX',
          'Jasper, TX',
          'Houston, TX',
          'Mason, TX',    
          'Sabinal, TX',
          'Laredo, TX',
          'Corpus Christi, TX',
          'McAllen, TX',
          'Odessa, TX',
          'Juno, TX',
          'Marfa, TX',
          'Cornudas, TX',
          'Terlingua']


def main():
    browser = webdriver.Firefox()
    with open('tx-clinics.csv', 'w') as csvfile:
        for i in range(cities):
            browser.get('https://www.healthytexaswomen.org/find-a-doctor')
            setup_page(browser)
            input = browser.find_element_by_id('form-field-address')
            input.send_keys(cities[i])
            input.submit()
            process_page(browser, csvfile)
            time.sleep(5)

# Prepares the parameters of radius 100 miles and which program to choose
def setup_page(browser):
    radius_id = "form-field-distance"
    radius_val = 100
    
    cancer_cbox = "form-field-services-option-4"
    medicaid_cbox = "form-field-services-option-5"
    
    #Tries to select 100 mile radius option
    try_radius(browser, radius_id, radius_val)
    
    #Tries to unselect the checkboxes
    try_cbox(browser, cancer_cbox)
    try_cbox(browser, medicaid_cbox)
       
# Finds and selects the radius
def try_radius(browser, form_id, radius_val):
    for i in range(10):
        try:
            select = Select(browser.find_element_by_id(form_id))
            select.select_by_visible_text('within ' + str(radius_val) + ' miles')
            break
        except NoSuchElementException as e:
            print('retry in 1s.')
            time.sleep(1)
    else:
        print("Cannot find checkbox: " + form_id)
        raise NoSuchElementException
        
    
# Finds and unchecks certain checkbox forms
def try_cbox(browser, form_id):
    for i in range(10):
        try:
            form = browser.find_element_by_id(form_id)
            if form.is_selected():
                form.click()
            break
        except NoSuchElementException as e:
            print('retry in 1s.')
            time.sleep(1)
    else:
        print("Cannot find checkbox: " + form_id)
        raise NoSuchElementException
        
# Parses the page for name, address, phone number, programs served, 
# and language
def process_page(browser, csvfile):
    writer = csv.DictWriter()
    
if __name__ == '__main__':
    main()