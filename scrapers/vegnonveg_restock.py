import requests
from bs4 import BeautifulSoup

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType

from setup import KEYWORDS

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()


software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)


headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}

last = []


def vegnonRestock():
    prod_list = []
    for pg in range(2, 50):
        URL = f"https://www.vegnonveg.com/footwear?page={pg}"
        try:
            s = requests.Session()
            page = s.get(url=URL, headers=headers)
            soup = BeautifulSoup(page.content, 'lxml')
            div_id = soup.find("div", id="products")
            products = div_id.find_all(
                "div", class_="product col-4-12 col-md-3-12")

            for product in products:
                info_str = ""
                prod_name = product.find("span", class_="p-name").text
                for k in KEYWORDS:
                    if k.lower() in prod_name.lower():

                        img_src = product.find(
                            "a", class_="gt-product-click").find('img')['src']
                        link = product.find(
                            "a", class_="gt-product-click")['href']
                        size = find_size(link)

                        info = product.find("div", class_="info mt-10")
                        paras = info.find_all("p")
                        for p in paras:
                            if p.text.strip() != "":
                                info_str += f"^{p.text.strip()}"
                        info_str = info_str.split("^")
                        prod_info = {"id": link.split("/")[-1].strip(), "company": info_str[1],
                                     "prod_name": prod_name, "price": info_str[3], "link": link, "size": size, 'img': img_src}
                        prod_list.append(prod_info)

        except:
            return prod_list

    return prod_list


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


# def update_database():
#     for p in vegnonRestock():
#         db.collection('vegnonveg').document(p['id']).set(p)


if __name__ == "__main__":
    print(vegnonRestock())
