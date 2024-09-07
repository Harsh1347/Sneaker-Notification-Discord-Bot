import requests
from bs4 import BeautifulSoup

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType

from setup import KEYWORDS

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)


headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}

last = []


def vegnon():

    URL = f"https://www.vegnonveg.com/footwear?sort=published_at&order_by=desc"
    s = requests.Session()
    page = s.get(url=URL, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    div_id = soup.find("div", id="products")
    products = div_id.find_all(
        "div", class_="product col-4-12 col-md-3-12")
    exist = []
    for product in products:
        info_str = ""
        img_src = product.find(
            "a", class_="gt-product-click").find('img')['src']
        link = product.find("a", class_="gt-product-click")['href']
        id = link.split("/")[-1]
        size = find_size(link)

        info = product.find("div", class_="info mt-10")
        paras = info.find_all("p")
        for p in paras:
            if p.text.strip() != "":
                info_str += f"^{p.text.strip()}"
        info_str = info_str.split("^")
        prod_info = {"id": id, "company": info_str[1],
                     "prod_name": info_str[2], "price": info_str[3], "link": link, "size": size, 'img': img_src}
        exist.append(prod_info)
    return exist


def find_size(prod_link):
    s = requests.Session()
    page = s.get(url=prod_link, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    try:
        size_table = soup.find("div", class_="dropdown")
        measure_scale = size_table.find(
            "ul", class_="dropdown-menu").find_all("li")
        sizes = [size.text for size in measure_scale]
        return sizes
    except:
        try:
            return [soup.find('p', class_='mt-10 red h1').text.strip()]
        except:
            return ["Sold Out"]


if __name__ == "__main__":
    print(vegnon())
