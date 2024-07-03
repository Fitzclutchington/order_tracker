import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL of the webstore with pagination placeholder
base_url = 'https://example.com/store?page={}'

# List to store scraped data
data = []

# Iterate through pages
for page in range(1, 11):  # Adjust the range as needed
    url = base_url.format(page)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all items on the current page
    items = soup.find_all('div', class_='item-class')  # Adjust the tag and class

    for item in items:
        try:
            # Extract desired attributes (adjust selectors as needed)
            name = item.find('h2', class_='item-name').text.strip()
            price = item.find('span', class_='item-price').text.strip()
            weight = item.find('span', class_='item-weight').text.strip()
            
            # Store the data in a dictionary
            item_data = {
                'name': name,
                'price': price,
                'weight': weight
            }
            
            # Append to the list
            data.append(item_data)
        except AttributeError as e:
            print(f"Error parsing item: {e}")
            continue
    
    # Respectful scraping by adding a delay
    time.sleep(2)

# Convert to DataFrame (optional)
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('webstore_items.csv', index=False)

print("Scraping complete. Data saved to 'webstore_items.csv'.")