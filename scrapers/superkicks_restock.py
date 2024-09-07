from setup import KEYWORDS
from bs4 import BeautifulSoup
import time
import os

from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType
import cloudscraper

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)

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


URL = f"https://superkicks.in/heat/"
headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}

scraper = cloudscraper.create_scraper()


def sk_restock():
    prod_list = []
    soup = BeautifulSoup(scraper.get(URL).text, "lxml")
    items = soup.find_all("div", class_="sk-col")
    for i in items:
        prod = {}
        prod['prod_name'] = (i.find("div", class_="sk-title").text)
        for k in KEYWORDS:
            if k.lower() in prod['prod_name'].lower():
                prod['link'] = (
                    i.find("div", class_="sk-title").find('a')['href'])
                prod['id'] = prod['link'].split("/")[-2].strip()
                prod['img'] = (
                    i.find("div", class_="sk-img").find("img")['src'])
                prod['price'] = None
                try:
                    prod['price'] = (
                        i.find("div", class_="sk-price sk-wc-vp").text)
                except:
                    prod['price'] = (i.find("div", class_="sk-price").text)
                prod['size'] = [
                    i.find("span", class_="bdt-position-relative").text]
                prod_list.append(prod)
                break
    non_heat = sk_all()
    prod_list.extend(non_heat)

    return prod_list


def sk_all():
    prod_list = []
    for pg in range(1, 50):
        try:
            URL = f"https://superkicks.in/product-category/footwear?sf_paged={pg}"
            soup = BeautifulSoup(scraper.get(URL).text, "lxml")
            ul = soup.find_all("div", class_="woocommerce-image__wrapper")
            for d in ul:
                prod = {}
                prod['prod_name'] = d.find("a")['aria-label']
                for k in KEYWORDS:
                    if k.lower() in prod['prod_name'].lower():
                        prod['link'] = (d.find("a")['href'])
                        prod['id'] = prod['link'].split("/")[-2].strip()
                        prod['img'] = (d.find("img")['src'])
                        prod['measure_scale'], prod['size'], prod['price'] = (
                            find_size(d.find("a")['href']))
                        prod_list.append(prod)
                        break
        except:
            return prod_list
    return prod_list


def find_size(prod_link):
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), chrome_options=set_chrome_options())

    # driver = webdriver.Firefox(options=options)
    driver.get(prod_link)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()
    driver.quit()
    size_table = soup.find("table", class_="variations")
    price = soup.find('p', class_="price").text
    try:
        measure_scale = size_table.find("td", class_="label").text
        sizes = [size.text for size in size_table.find(
            "ul", class_="variable-items-wrapper button-variable-wrapper").find_all("li") if size['class'][-1] != 'disabled']
        options = soup.find("select", id="pa_shoe-size-uk")

        return measure_scale, sizes, price

    except:
        try:

            options = soup.find("select", id="pa_shoe-size-uk")
            sizes = [o.text for o in options.find_all(
                "option") if 'option' not in o.text]
            return "UK", sizes, price
        except:
            return "UK", ['Sold Out'], price


if __name__ == "__main__":
    print((sk_restock()))
