#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 09:19:50 2017

A simple script that grabs all the available zip codes in Texas and outputs
them into a file for further processing.

@author: Steve Wang
"""
from bs4 import BeautifulSoup

import re
import requests

def script():
    
    #Used to spoof user agent in order to web scrape, optional for this site
    url = 'http://www.zipcodestogo.com/Texas/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 '
               'Safari/537.36'}
    
    r = requests.get(url, headers=headers)
    
    #Catches for errors in obtaining zip codes
    try:
        r.raise_for_status()
    except Exception as exc:
        print('There was problem retrieving the zip website: %s' % (exc))
        
    valid_zip = re.compile(r"\d\d\d\d\d")
    
    parser = BeautifulSoup(r.text)
    
    #Iterates through the html document and prints out zip codes in Texas
    with open('zip.txt', 'w') as f:
        for link in parser.find_all('a'):
            soup_string = str(link.string)
            if (valid_zip.match(soup_string)):
                f.write(soup_string)
                f.write('\n')
                
if __name__ == '__main__':
    script()