# %%
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time
import urllib.parse
import random

# %% [markdown]
# 1. Set up Selenium

# %%
url = "https://minibardelivery.com/store/search/organic%2Bwine?q=organic%2520wine"
driver = webdriver.Chrome("//Users/irene/CloudStation/Courses/Digital Technologies and Value Creation/Group Project/US/Group 3/Codes/Data scraping/chromedriver")
driver.get(url)

# %% [markdown]
# Scroll down page

# %%
SCROLL_PAUSE_TIME = 4

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# %% [markdown]
# Comebine Selenium & Beautifulsoup

# %%
page_source = driver.page_source
page_source 

# %%
soup = BeautifulSoup(page_source , "html.parser")
print(soup.prettify())

# %% [markdown]
# 2. Scraping

# %%
name_list = []
price_list = []
delivery_time_list = []
for item in soup.findAll('li',class_='ProductTile_element__KRgs2'):
    
    #item title
    itemname = item.find('div',class_='ProductTileName_element__v8rIj').text
    name_list.append(itemname)
    
    #item price
    item_prices = item.find('div',class_="ProductTilePrice_element__RFvI_")
    item_price = item_prices.find('span',class_="ProductTilePrice_notDiscountSale__QG6dy").text
    price_list.append(item_price)

    #delivery time
    delivery_time = item.find('div',class_="DeliveryMethod_element__7MV6t").text
    delivery_time_list.append(delivery_time)
    
    #end
itemdf = pd.DataFrame({'Name': name_list,'Prices': price_list, "Deliverytime": delivery_time_list})

# %%
itemdf.to_csv("scrapingresult.csv")