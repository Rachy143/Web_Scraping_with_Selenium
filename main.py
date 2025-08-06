from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time


chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://snapklik.com/")

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CLASS_NAME, "mat-typography"))
    )

input_element = driver.find_element(By.CLASS_NAME, "mat-typography")
input_element.clear
input_element.send_keys("Beauty & Personal care" + Keys.ENTER)

WebDriverWait(driver, 15).until()
EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Beauty & Personal care"))

link = driver.find_elements(By.PARTIAL_LINK_TEXT, "Beauty & Personal care")
link_click()

time.sleep(10)

driver.quit()
