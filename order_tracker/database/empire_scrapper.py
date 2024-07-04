import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Base URL of the webstore with pagination placeholder
base_url = "https://empiresafe.com/pre-owned/all/"

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

size_keys = [
    "INSIDE DIMENSIONS",
    "OUTSIDE DIMENSIONS",
    "CAPACITY",
    "WEIGHT",
]

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU usage (optional)
chrome_options.add_argument("--window-size=1920x1080")  # Set the window size (optional)
driver = webdriver.Chrome(options=chrome_options)


# Iterate through pages
# TODO: don't hard code this
for page_num in range(1, 10):
    url = f"{base_url}?fwp_paged={page_num}"
    driver.get(url)
    
    # Wait for the items to be present
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.entry-content ul li.fwp-product"))
        )
    except:
        print(f"Items not found on page {page_num}")
        continue
    
    items = driver.find_elements(By.CSS_SELECTOR, "div.entry-content ul li.fwp-product")

    # only click metrics button once
    if page_num == 1:
        toggle_button = items[0].find_element(By.CSS_SELECTOR, "div.metSwap a span.lblMet")
        toggle_button.click()
        time.sleep(1)

    for item in items:
        
        item_data = {}
        image = item.find_element(By.TAG_NAME, "img").get_attribute("src")
        item_data["image"] = image

        table = item.find_element(By.CSS_SELECTOR, "table.dimTbl")
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            header = row.find_element(By.TAG_NAME, "th").text.strip()
            if header in valid_keys:
                if header in size_keys:
                    item_data[header] = row.find_element(
                        By.CSS_SELECTOR, "td span.met"
                    ).text.strip()
                else:
                    item_data[header] = row.find_element(By.TAG_NAME, "td").text.strip()

        price_content = item.find_element(By.CSS_SELECTOR, "p.fwp-price span.amount")
        price_text = driver.execute_script(
            "return arguments[0].textContent", price_content
        ).strip()
        item_data["price"] = price_text

        # Append to the list
        data.append(item_data)

    # Respectful scraping by adding a delay
    time.sleep(5)

df = pd.DataFrame(data)

file_path = Path(__file__).resolve()
top_level_dir = file_path.parent
df.to_csv(top_level_dir / "sample_data" / "items.csv", index=False)
