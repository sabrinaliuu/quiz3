from selenium import webdriver # for controlling website
from bs4 import BeautifulSoup # get html elements
import time
from selenium.webdriver.common.by import By 
import pandas as pd
import requests
import json

driver = webdriver.Chrome()
driver.get('https://www.tmnewa.com.tw/ec/travel/overseas/count1') 
soup = BeautifulSoup(driver.page_source, 'html.parser')

# get country
all_country = soup.select('div.tabs-component-panels section')[1:]
results = []

for section in all_country:
    countries = [
        li.get_text(strip=True).replace("(申根國)", "") 
        for li in section.select('ul.countryList li')
    ]
    results.extend(countries)
print(results)
