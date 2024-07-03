import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Base URL of the webstore with pagination placeholder
base_url = "https://empiresafe.com/pre-owned/all/?fwp_paged="

# List to store scraped data
data = []

valid_keys = [
    "MANUFACTURER",
    "SERIES",
    "FIRE PROTECTION",
    "MODEL",
    "INSIDE DIMENSIONS",
    "OUTSIDE DIMENSIONS",
    "CAPACITY",
    "WEIGHT",
    "SWING",
]

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--disable-gpu')  # Disable GPU usage (optional)
chrome_options.add_argument('--window-size=1920x1080')  # Set the window size (optional)
driver = webdriver.Chrome(options=chrome_options)


# Iterate through pages
# TODO: don't hard code this
for page_num in range(1, 10):
    url = f"{base_url}{page_num}"
   
    driver.get(url)
    html = driver.page_source
    
    items = driver.find_elements(By.CSS_SELECTOR, "div.entry-content ul li.fwp-product")

    for item in items:
        item_data = {}
        image = item.find_element(By.TAG_NAME, "img").get_attribute("src")
        item_data["image"] = image

        table = item.find_element(By.CSS_SELECTOR, "table.dimTbl")
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            header = row.find_element(By.TAG_NAME, "th").text.strip()
            if header in valid_keys:
                item_data[header] = row.find_element(By.TAG_NAME, "td").text.strip()

        price_content = item.find_element(By.CSS_SELECTOR, "p.fwp-price span.amount")
        if price_content:
            pass
        else:
            item_data["price"] = price_content.text.strip()
        # Append to the list
        data.append(item_data)

    # Respectful scraping by adding a delay
    time.sleep(5)

print(data)