#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 09:19:50 2017

A simple script that grabs all the available zip codes in Texas and outputs
them into a file for further processing.

@author: Steve Wang
"""
from bs4 import BeautifulSoup

import sys
import requests

url = 'http://www.zipcodestogo.com/Texas/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r = requests.get(url, headers=headers)

try:
    r.raise_for_status()
except Exception as exc:
    print('There was problem retrieving the zip website: %s' % (exc))
    
parser = BeautifulSoup()

print(r.text)