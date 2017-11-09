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

from bs4 import BeautifulSoup

import csv
import re
import time
import lxml

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
          'Terlingua, TX']


def main():
    browser = webdriver.Firefox()
    with open('tx-clinics.csv', 'w', newline='') as csvfile:
        clinics_seen = set()
        fieldnames = ['Name', 'Address', 'Phone Number', 
                       'Programs Served', 'Languages Spoken']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(cities)):
            browser.get('https://www.healthytexaswomen.org/find-a-doctor')
            setup_page(browser)
            time.sleep(5)
            input = browser.find_element_by_id('form-field-address')
            input.send_keys(cities[i])
            input.submit()
            time.sleep(5)
            process_page(browser, writer, csvfile, clinics_seen)

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
        print("Cannot find radius dropdown: " + form_id)
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
def process_page(browser, writer, csvfile, clinics_seen):
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    names = []
    address = []
    phone_number = []
    programs = []
    languages = []
    
    for clinic_name in soup.find_all("div", class_="name"):
        names.append(clinic_name.get_text().strip())
    
    for full_address in soup.find_all("span", class_="full-address"):
        address.append(full_address.get_text(separator=' '))
        
    for phone in soup.find_all("span", class_="phone"):
        phone_number.append(phone.get_text().strip())
    
    for span in soup.find_all("span", class_="info-label"):
        if (span.text == "Programs Served: "):
            programs.append(span.next_sibling.strip())
        if (span.text == "Languages Spoken: "):
            languages.append(span.next_sibling.strip())
    
    for i in range(len(names)):
        if names[i] not in clinics_seen:
            writer.writerow({'Name' : names[i], 
                             'Address' : address[i], 
                             'Phone Number' : phone_number[i],
                             'Programs Served' : programs[i],
                             'Languages Spoken' : languages[i]
                             })
            clinics_seen.add(names[i])
            clinics_seen.add(address[i])
    
if __name__ == '__main__':
    main()