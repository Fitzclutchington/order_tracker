import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


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

# Iterate through pages
# TODO: don't hard code this
for page_num in range(1, 10):
    url = f"{base_url}{page_num}"
    print(url)
    response = requests.get(url)
    print(response)
    if response.status_code != 202:
        print(f"Failed to retrieve page {page_num}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")

    # Find all items on the current page
    item_div = soup.find("div", class_="entry-content")
    item_list = item_div.find("ul")
    items = item_list.find_all("li", class_="fwp-product")

    for item in items:
        item_data = {}
        image = item.find("img").get("src")
        item_data["image"] = image

        item_content = item.find("table", class_="dimTbl")
        rows = item_content.find_all("tr")

        for row in rows:
            header = row.find("th").text.strip()
            if header in valid_keys:
                item_data[header] = row.find("td").text.strip()

        price_content = item_content.find("p", class_="fwp-price")
        if price_content.find("span", class_="woocommerce-Price-amount amount"):
            pass
        else:
            item_data["price"] = price_content.find("span", class_="amount").text.strip()
        # Append to the list
        data.append(item_data)

    # Respectful scraping by adding a delay
    time.sleep(5)

print(data)