from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from setup import KEYWORDS


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)

headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}


def ajioApi():
    s = requests.Session()
    products = []
    res = s.get(r'https://www.ajio.com/api/category/830207010?fields=SITE&currentPage=0&pageSize=100&format=json&query=%3Anewn&sortBy=newn%3Abrand%3ANIKE',
                headers=headers).json()
    res2 = s.get("https://www.ajio.com/api/category/830207010?fields=SITE&currentPage=0&pageSize=100&format=json&query=%3Anewn&sortBy=newn%3Abrand%3AAdidas%20Originals%3Abrand%3AADIDAS", headers=headers).json()
    for p in res['products']:
        product = {}
        product['prod_name'] = (p['name'])
        product['img'] = (p['images'][0]['url'])
        product['price'] = (p['price']['displayformattedValue'])
        product['company'] = (p['fnlColorVariantData']['brandName'])
        product['link'] = ("https://www.ajio.com"+p['url'])
        api_url = ("https://www.ajio.com/api/" +
                   "/".join(p['url'].split('/')[-2:]))
        product['id'] = api_url.split('/')[-1]
        product['size'] = (find_size(api_url))
        products.append(product)

    for p in res2['products']:
        product = {}
        product['prod_name'] = (p['name'])

        product['img'] = (p['images'][0]['url'])
        product['price'] = (p['price']['displayformattedValue'])
        product['company'] = (p['fnlColorVariantData']['brandName'])
        product['link'] = ("https://www.ajio.com"+p['url'])
        api_url = ("https://www.ajio.com/api/" +
                   "/".join(p['url'].split('/')[-2:]))
        product['id'] = api_url.split('/')[-1]
        product['size'] = (find_size(api_url))
        products.append(product)
    return products


def find_size(url):
    s = requests.Session()
    res = s.get(url, headers=headers, verify=False).json()
    sizes = []

    if res['stock']['stockLevelStatus'] == 'outOfStock':
        return sizes

    try:
        for v in res['variantOptions']:
            if v['stock']['stockLevel'] != 0:
                try:
                    sizes.append(
                        f"{v['displaySizeFormat']} {v['scDisplaySize']}")
                except:
                    sizes.append(
                        f"{v['displaySizeFormat']} {v['variantOptionQualifiers'][4]['value']}")
        return sizes
    except:
        print("no varianats found", url)
        return ['size info not available']


if __name__ == "__main__":
    print(ajioApi())
