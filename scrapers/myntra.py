import requests
import json
import datetime as dt
from bs4 import BeautifulSoup

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType

from fp.fp import FreeProxy

from setup import KEYWORDS

proxy = FreeProxy(country_id=['IN']).get()

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)


head1 = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
         'Accept': 'application/json',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.5',
         'Connection': 'keep-alive'
         }


def myntra_data():
    print(dt.datetime.now().time())
    products = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    s = requests.Session()
    try:
        for pg in range(1, 15):
            res = s.get(
                f"https://www.myntra.com/men-sneakers?f=Brand%3AADIDAS%2CADIDAS%20NEO%2CADIDAS%20Originals%2CNike&p={pg}&plaEnabled=false&sort=new",
                headers=head1, )  # proxies=proxyDict)

            soup = BeautifulSoup(res.text, "lxml")
            script = None
            for i in soup.find_all("script")[11]:
                script = i
            data = dict(json.loads(script[script.index('{'):]))

            productData = data['searchData']['results']['products']

            for prod in productData:
                product = {}
                product['prod_name'] = (prod['product'])
                product['id'] = (prod['productId'])
                if pg == 1:
                    product['link'] = ("https://www.myntra.com/" +
                                       prod['landingPageUrl'])
                    product['company'] = (prod['brand'])
                    product['img'] = (prod['images'][0]['src'])
                    product['price'] = (prod['price'])
                    product['size'] = ([i['label']
                                        for i in prod['inventoryInfo'] if i['available'] == True])
                    products.append(product)

                else:
                    for k in KEYWORDS:
                        if k.lower() in product['prod_name'].lower():
                            product['link'] = ("https://www.myntra.com/" +
                                               prod['landingPageUrl'])
                            product['company'] = (prod['brand'])
                            product['img'] = (prod['images'][0]['src'])
                            product['price'] = (prod['price'])
                            product['size'] = ([i['label']
                                                for i in prod['inventoryInfo'] if i['available'] == True])
                            products.append(product)
    except Exception as e:
        return products

    return products


if __name__ == "__main__":
    print(myntra_data())
