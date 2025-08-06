from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv

# Setup Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Setup WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to Snapklik skincare page
driver.get("https://snapklik.com/en-bb/g/c/beauty-health?id=3760911")

wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'app-grid-card')))

# Find all product cards
product_cards = driver.find_elements(By.CSS_SELECTOR, 'app-grid-card')
print(f"Found {len(product_cards)} products")

product_data = []

# Extract product URLs
for card in product_cards:
    try:
        link_elem = card.find_element(By.TAG_NAME, 'a')
        link = link_elem.get_attribute("href")
        if link:
            product_data.append({"url": link})
    except Exception as e:
        print(f" Could not extract URL from card: {e}")

# Visit each product page
for product in product_data:
    driver.get(product['url'])

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))

        def safe_find(by, selector):
            try:
                return driver.find_element(by, selector).text
            except:
                return ''

        product['Product ID'] = product['url'].split('/')[-1]
        product['Product Name'] = safe_find(By.CSS_SELECTOR, 'h1')
        product['Brand Name'] = safe_find(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(2) > td:nth-child(2)')
        product['Product Description'] = safe_find(By.CSS_SELECTOR, 'app-features > div > ul')
        product['Price'] = safe_find(By.CSS_SELECTOR, 'span.product-price.large')
        product['Ingredients'] = safe_find(By.XPATH, '//div[contains(text(), "Ingredients")]/following-sibling::div')
        product['Skin Concern'] = safe_find(By.XPATH, '//div[contains(text(), "Skin Concern")]/following-sibling::div')
        product['Size/Volume'] = safe_find(By.CSS_SELECTOR, 'div.row.product-columns.gap_20 > div:nth-child(1) > div > p > span')
        product['Barcode'] = safe_find(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(3) > td:nth-child(2)')
        product['Item Weight'] = safe_find(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > td:nth-child(2)')
        product['Size/Volume'] = safe_find(By.CSS_SELECTOR, 'app-option:nth-child(1) > div.row.space-between.v-center-flex.mt_20.mb_6 > p')
        product['UPC'] = safe_find(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(4) > td:nth-child(2)')
        product['Source URL'] = product['url']

        try:
            image_element = driver.find_element(By.CSS_SELECTOR, 'img')
            product['Product Images'] = image_element.get_attribute('src')
        except:
            product['Product Images'] = ''

        print(f" Extracted: {product['Product Name']}")

    except Exception as e:
        print(f" Error extracting {product['url']}: {e}")

# Save data to CSV
with open('snapklik_products.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = product_data[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_data)

# Done
driver.quit()
