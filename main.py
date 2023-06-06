import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up ChromeDriver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Update the driver path with your custom path
driver_path = "D:/chrome driver/chromedriver.exe"

# Start the ChromeDriver service
service = Service(driver_path)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the URL to scrape
url = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/krakow?distanceRadius=0&priceMin=200000&priceMax=500000&areaMin=40&areaMax=80&locations=%5Bcities_6-38%5D&viewType=listing&limit=72&page=1"

# Navigate to the URL
driver.get(url)

# Wait for the page to load
time.sleep(3)

# Scroll to the bottom of the page to trigger lazy loading
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Wait for lazy-loaded elements to be visible
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "css-iq9jxc")))

# Get the page source
page_source = driver.page_source

# Close the driver
driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Find all the offer items
offer_items = soup.find_all("li", class_="css-iq9jxc")

# Iterate over the offer items and extract the URLs
districts = ['Dębniki', 'Ludwinów', 'Stare Podgórze', 'Krowodrza', 'Nowa Wieś', 'Nowy Świat', 'Salwator']
max_price_per_sqm = 11000

urls = []
for item in offer_items:
    link = item.find("a", class_="css-1up0y1q")
    if link:
        url = link["href"]
        location = item.find("p", class_="css-14aokuk e1ualqfi4").text
        district = None
        for dist in districts:
            if dist in location:
                district = dist
                break

        if district is not None:
            price_per_sqm_element = item.find("span", string=lambda text: text and "/m²" in text)
            if price_per_sqm_element:
                price_per_sqm = ''.join(filter(str.isdigit, price_per_sqm_element.text.replace('\xa0', ' ').replace('²', '')))
                if price_per_sqm.isdigit() and float(price_per_sqm) <= max_price_per_sqm:
                    urls.append(url)

# Print the URLs
for url in urls:
    print(url)
