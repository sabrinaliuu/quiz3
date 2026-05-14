from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from generate_random_data import generate_random_data
from select_calendar_date import select_calendar_date

import json
from time import sleep
import os
import sys


### get path (for packing .exe) ###
def get_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

### init for webdriver ###
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://www.tmnewa.com.tw/ec/travel/overseas/count1') 
wait = WebDriverWait(driver, 10, 1)

### load data ###
form_data = generate_random_data()
# json.load(open(get_path("../data/test.json"), "r", encoding="utf-8"))
# print(form_data)

### start processing ###
# 開始填寫表單

## 保險對象: peopleTab ##
driver.find_element(By.CLASS_NAME, "people_tab_accu"+form_data["peopleTab"]).click()
sleep(1)
driver.find_element(By.CLASS_NAME, "people_confirm_accu"+form_data["peopleTab"]).click()
sleep(0.5)

## 旅遊國家: travelCountry ##
# scroll to 
element = driver.find_element(By.CLASS_NAME, "topBtn")
driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 60);", element)
sleep(1)
# key in 各國家
input_box = driver.find_element(By.CSS_SELECTOR, "input.ti-valid.ti-new-tag-input")
for country in form_data["travelCountry"]:
    input_box.send_keys(country)
    sleep(1) 
    input_box.send_keys(Keys.ENTER)
sleep(3)

## 投保人數與年齡: peopleCount ##
driver.find_element(By.CSS_SELECTOR, "input.clarity-unmask").click()

# 取得各個年齡層人數控制按鈕
buttons = driver.find_elements(By.CSS_SELECTOR, "img[src='/ec/travel/overseas/img/plus.f343272d.svg']")

# 選擇各個年齡層人數
for person in form_data["peopleCount"]:
    for category, count in person.items():
        for _ in range(count):
            sleep(0.5)
            if category == "elderCount":
                buttons[0].click()
            elif category == "adultCount":
                buttons[1].click()
            elif category == "youthCount":
                buttons[2].click()
            elif category == "childCount":
                buttons[3].click()
            elif category == "babyCount":
                buttons[4].click()    
sleep(1)
driver.find_element(By.CLASS_NAME, "close").click()
sleep(1)


## 出發日與返回日 ##
driver.find_element(By.CSS_SELECTOR,"div.startDate input").click()
select_calendar_date(driver, form_data['startDate'])
sleep(1)

driver.find_element(By.CSS_SELECTOR,"div.endDate input").click()
select_calendar_date(driver, form_data['endDate'])
sleep(1)

## 時間 ##
driver.find_element(By.ID, "timeSelect").click()
driver.find_element(By.CSS_SELECTOR, "[value='"+form_data["time"]+"']").click()
sleep(3)

## submit form: 試算保費 ##
driver.find_element(By.CLASS_NAME, "count1_go_accu").click()
sleep(3)

## 保期確認modal ##
wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "date_confirm_accu"))
).click()
sleep(3)

## 投保審核modal ##
# 部分國家無法加購海外突發疾病險，包含這些國家時才會出現此modal
try:
    optional_button =  WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "swal2-confirm"))
    )
    optional_button.click()
except:
    pass
sleep(5)


## 查看保費 ##
result_element =  wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "p.Price.clarity-unmask"))
)
driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 150);", result_element)
print(result_element.text)

sleep(60)