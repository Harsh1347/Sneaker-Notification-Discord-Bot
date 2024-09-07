import requests
import json
import re

from setup import KEYWORDS


def nike_new():
    uri = 'https://www.nike.com/in/w/new-shoes-3n82yz3rauvz5e1x6znik1zy7ok?sort=newest'

    base_url = 'https://api.nike.com'
    session = requests.Session()

    def get_lazy_products(stub, products):
        response = session.get(base_url + stub).json()
        next_products = response['pages']['next']
        products += response['objects']
        if next_products:
            get_lazy_products(next_products, products)
        return products

    html_data = session.get(uri).text
    redux = json.loads(
        re.search(r'window.INITIAL_REDUX_STATE=(\{.*?\});', html_data).group(1))

    wall = redux['Wall']
    initial_products = re.sub(
        'anchor=[0-9]+', 'anchor=0', wall['pageData']['next'])

    products = get_lazy_products(initial_products, [])

    cloudProductIds = set()
    unique_products = []
    for product in products:
        try:
            if not product['id'] in cloudProductIds:
                cloudProductIds.add(product['id'])
                unique_products.append(product)
        except KeyError:
            print(product)

    products_list = []

    for p in unique_products:
        product_info = {}

        product_info['id'] = p['productInfo'][0]['merchProduct']['id']
        product_info["prod_name"] = (
            p['productInfo'][0]['merchProduct']['labelName'])

        product_info["link"] = ("https://www.nike.com/in/u/" +
                                p['publishedContent']['properties']['seo']['slug'])
        product_info["price"] = (
            p['productInfo'][0]['merchPrice']['currentPrice'])
        product_info["img"] = (p['publishedContent']['properties']
                               ['productCard']['properties']['squarishURL'])
        product_info["color"] = (p['productInfo'][0]
                                 ['productContent']['colorDescription'])
        product_info["size"] = (str(p['productInfo'][0]
                                     ['availability']['available']))
        products_list.append(product_info)
    return products_list


if __name__ == "__main__":
    print(len(nike_new()))
