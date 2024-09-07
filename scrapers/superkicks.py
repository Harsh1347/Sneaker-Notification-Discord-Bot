from setup import KEYWORDS
import requests
from bs4 import BeautifulSoup
from fp.fp import FreeProxy
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType
import cloudscraper

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)
proxy = FreeProxy(rand=True).get()

scraper = cloudscraper.create_scraper()

URL = "https://superkicks.in/product-category/footwear/"
headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}


last = []


def superkick():

    soup = BeautifulSoup(scraper.get(URL).text, "lxml")
    ul = soup.find("ul", class_="products columns-3")

    products = ul.find_all("li")

    exist = []
    for product in products:
        img_src = product.find("a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link").find(
            "img", class_="gallery-image wp-post-image")['src']
        link = product.find(
            "a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")['href']

        measure_scale, sizes = find_size(link)
        info = product.find("div", class_="woocommerce-card__header")
        brand = info.find("small", class_='brand').text
        prod_name = info.find(
            "div", class_='woocommerce-loop-product__title').text
        price = info.find("span", class_="price").text
        id = link.split("/")[-2]
        prod_info = {"id": id,
                     "prod_name": prod_name, "price": price, "link": link, "measure_scale": measure_scale, 'size': sizes, 'img': img_src}
        exist.append(prod_info)

    return exist


def find_size(prod_link):
    soup = BeautifulSoup(scraper.get(prod_link).text, "lxml")
    size_table = soup.find("table", class_="variations")
    try:
        measure_scale = size_table.find("td", class_="label").text
        sizes = [size.text for size in size_table.find(
            "ul", class_="variable-items-wrapper button-variable-wrapper").find_all("li")]
        return measure_scale, sizes

    except:
        try:

            options = soup.find("select", id="pa_shoe-size-uk")
            sizes = [o.text for o in options.find_all(
                "option") if 'option' not in o.text]
            return "UK", sizes
        except:
            return "UK", ['Sold Out']


if __name__ == "__main__":

    print(superkick())
