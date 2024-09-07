from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os

from setup import KEYWORDS

options = FirefoxOptions()
options.add_argument("--headless")


def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOGGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options


def adidas():
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), chrome_options=set_chrome_options())
    #driver = webdriver.Firefox(options=options)
    driver.get(
        r"https://shop.adidas.co.in/#category/Pag-120/No-0/activeStartDate_dtdesc/All/NOT%20maxDiscountPercent_d:[0%20100]%20AND%20_facet_.GENDER_FACET_ss:(%22MEN%22)%20AND%20_facet_.DIVISION_CATEGORY_ss:(%22FOOTWEAR%22)%20AND%20_facet_.PRODUCT_TYPE_GROUP_ss:(%22SHOES%22)%20AND%20allBrands_ss:(%22ORIGINALS%22)")
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()
    driver.quit()
    ul = soup.find_all("li", class_="col-md-3 img-thumbnail card")
    products = []
    for l in ul:
        id = l.find(
            "span", class_="card-size-select")['data-default-productid']
        link = l.find("a", class_="productIdentifier productImageWrap")['href']
        try:
            img_src = l.find("img", class_="lazy img-responsive")['data-src']
        except:
            continue
        prod_name = (
            l.find("a", class_="adidasOriginals productIdentifier").text)
        if "Kids".lower() in prod_name.lower() or "Baby" in prod_name.lower():
            continue
        price = (l.find("span", class_="PLPPrice").text).strip()
        sizes = l.find("span", class_="card-size-field").text.strip()
        sizes = sizes.split(')')[1].strip()
        size = []
        s = 0
        while s < len(sizes):
            el = sizes[s]
            if el == '1':
                size.append(el+sizes[s+1])
                s += 1
            else:
                size.append(el)
            s += 1
        if size == []:
            size = ['not available']
        products.append(
            {"id": id, "prod_name": prod_name, "price": price, "size": size, 'img': img_src, 'link': link})
    return products


if __name__ == "__main__":
    print(adidas())
