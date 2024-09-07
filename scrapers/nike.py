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


def nikeApi():
    items = []
    for page in [0, 60]:
        URL = f"https://api.nike.com/product_feed/threads/v2/?anchor={page}&count=60&filter=marketplace(IN)&filter=language(en-GB)&filter=inStock(true)&filter=productInfo.merchPrice.discounted(false)&filter=channelId(010794e5-35fe-4e32-aaff-cd2c74f89d61)&filter=exclusiveAccess(true%2Cfalse)&fields=active%2Cid%2ClastFetchTime%2CproductInfo%2CpublishedContent.nodes%2CpublishedContent.subType%2CpublishedContent.properties.coverCard%2CpublishedContent.properties.productCard%2CpublishedContent.properties.products%2CpublishedContent.properties.publish.collections%2CpublishedContent.properties.relatedThreads%2CpublishedContent.properties.seo%2CpublishedContent.properties.threadType%2CpublishedContent.properties.custom%2CpublishedContent.properties.title"
        products = requests.get(url=URL).json()
        for i in range(len(products['objects'])):
            product = {}
            product['id'] = products['objects'][i]['productInfo'][0]['merchPrice']['id']
            product['title'] = (products['objects'][i]['productInfo']
                                [0]['merchProduct']['labelName'])
            product['link'] = "https://www.nike.com/in/launch/t/"+(products['objects'][i]['publishedContent']
                                                                   ['properties']['seo']['slug'])
            product['price'] = (products['objects'][i]['productInfo']
                                [0]['merchPrice']['currentPrice'])
            product['img'] = (products['objects'][i]['productInfo']
                              [0]['imageUrls']['productImageUrl'])
            product['color'] = (products['objects'][i]['productInfo']
                                [0]['productContent']['colorDescription'])
            size_chart = {i['id']: i['nikeSize']
                          for i in products['objects'][i]['productInfo'][0]['skus']}

            product['size'] = [size_chart[i['skuId']] for i in products['objects'][i]['productInfo']
                               [0]['availableSkus'] if i['available'] == True]

            items.append(product)

    return items


def get_info(prod_link):
    try:
        s = requests.Session()
        page = s.get(url=prod_link, headers=headers, timeout=(3, 27))
        soup = BeautifulSoup(page.content, 'lxml')
        ul = soup.find(
            "ul", class_="size-layout bg-offwhite border-light-grey ta-sm-l z3 mb3-lg    ")
        print(ul)
        info_div = soup.find(
            "div", class_="product-info ncss-col-sm-12 full ta-sm-c")
        prod_name = info_div.find("h1").text
        prod_colour = info_div.find("h5").text
        price = info_div.find("div").text
        print(prod_name, prod_colour, price)
    except:
        pass


if __name__ == "__main__":
    print(len(set([d['id'] for d in nikeApi()])))
    print(len(([d['link'] for d in nikeApi()])))
    print(len([d['color'] for d in nikeApi()]))
    print(len([d['price'] for d in nikeApi()]))
    print(len([d['img'] for d in nikeApi()]))
    print(len([d['size'] for d in nikeApi()]))
