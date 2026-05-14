from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep

# date format: YYYY-MM-DD
def select_calendar_date(driver, target_date):

    wait = WebDriverWait(driver, 10, 1)

    # 分為年,月與網頁月曆比對
    target_year = target_date.split('-')[0]
    target_month = str(int(target_date.split('-')[1])) + "月"

    while True:
        sleep(2)

        # 取得目前顯示的年,月
        current_year_text = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mx-btn-current-year"))).text
        current_month_text = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mx-btn-current-month"))).text
  
        # 年月正確 -> 找日期 -> 點擊
        if current_year_text == target_year and current_month_text == target_month:

            date_selector = f"td.cell[title='{target_date}']:not(.disabled)"
            try:
                date_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, date_selector)))
                driver.execute_script("arguments[0].click();", date_element)
                break
            except:
                break
        
        # 年月不符 -> 點「下一個月」按鈕
        next_month_btn = driver.find_element(By.CLASS_NAME, "mx-btn-icon-right")
        next_month_btn.click()
        sleep(0.5)
