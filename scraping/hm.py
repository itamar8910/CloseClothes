import json

import requests
from bs4 import BeautifulSoup
from ScrapeProduct import ScrapeProduct
from utils import get_html_selenium, get_html

import pickle
from utils import get_html_selenium
from concurrent.futures import ThreadPoolExecutor

N_PRODUCTS = 0
N_SCRAPED = 0

class HMProduct(ScrapeProduct):
    def __init__(self, url, gender, soup=None):
        super().__init__(url, soup=soup)
        self.gender = gender

    def load_html(self):
        # return get_html_with_js(self.url)
        return get_html_selenium(self.url, verbose=True)

    def scrape_name(self):
        return self.soup.find('form', attrs={'id':'product'}).find('h1').contents[0]
        # return self.soup.find('div', attrs={'class': 'name'}).find('h1').contents[0]

    def scrape_price(self):
        return self.soup.find('span', attrs={'id': 'text-price'}).find('span').text

    def scrape_sizes(self): # TODO: this site denotes the range of the sizes, e.g S - L, but currently we'd only scrape S,L (without medium)
        return self.soup.find('span', attrs={'id':'text-selected-variant'}).text.strip().replace("SIZE","").split("-")

    def scrape_color(self):
        return self.soup.find('dl', attrs={'class':'options'}).findAll('dd')[0].find('span').text

    def scrape_description(self):
        return self.soup.find('div', attrs={'class':'description'}).find('p').text.strip()

    def scrape_imgs(self):
        return [li.find('a')['href'] for li in self.soup.find('ul', attrs={'id':'product-thumbs'}).findAll('li') if li.find('a')]

    def scrape_brand(self):
        return "H&M"

    def scrape_gender(self):
        return self.gender

    def __hash__(self):
        return self.url.__hash__()

    def __eq__(self,other):
        return self.url == other.url

    #Overriding
    @classmethod
    def scrape_category(cls,category_url,gender):
        base_products = super(HMProduct,cls).scrape_category(category_url,gender)
        color_products = list()
        with ThreadPoolExecutor() as executor:
            for product in base_products:
                color_products.extend(color_prod for color_prod in executor.map(lambda url:HMProduct(url,gender),get_all_color_variants_url_of_product(product)))
        return {product for product in base_products + color_products if not irrelevant_product(product)}

    def scrape_product_urls(html):
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.findAll('a', attrs={'class': 'product-url js-product-tracking js-product-tracking-initialized'})
        return [prod_box['href'] for prod_box in data]

        for prod_box in data:
            print(prod_box['href'])
            prod_soup = BeautifulSoup(get_html_selenium(prod_box['href']), 'html.parser')#TODO: don't get_html here, it breaks the parralelism of the outside
            prod_colors_urls = get_all_color_variants_url_of_product(prod_soup, prod_box['href'])
            print("color variants:", prod_colors_urls)
            for prod_color_url in prod_colors_urls:
                products.append(
                    {'url': prod_color_url,
                    'soup': prod_soup if prod_color_url != prod_box['href'] else None}
                )
        return [product['url'] for product in products if not irrelevant_product(HMProduct(**product,gender=''))]

def get_all_color_variants_url_of_product(prod : HMProduct):
    prod_soup = prod.soup
    prod_url = prod.url
    prod_base_url = prod_url[:prod_url.index('?article=')]
    all_colors = [prod_base_url + color_prod.find('a')['href'] for color_prod in prod_soup.find('ul', attrs={'id':'options-articles'}).findAll('li')]
    return [color_url for color_url in all_colors if color_url != prod_url]


def irrelevant_product(prod : HMProduct) -> bool:
    bad_names = ["trouses", "socks", "thong", "pants"]
    return any([x in prod.name.lower() for x in bad_names])



HM_CATEGORIES = {
        'Male': [
            "http://www.hm.com/il/products/men/jumpers_cardigans"]
        #      "http://www.hm.com/il/products/men/outerwear",
        #      "http://www.hm.com/il/products/men/shirts",
        #      "http://www.hm.com/il/products/men/tshirt",
        #      "http://www.hm.com/il/products/men/blazers_suits",
        #      "http://www.hm.com/il/products/men/hoodies_sweatshirt"
        #  ],
        #  'Female': [
        #      'http://www.hm.com/il/products/ladies/basics/tops',
        #      'http://www.hm.com/il/products/ladies/basics/cardigansjumpers',
        #      'http://www.hm.com/il/products/ladies/basics/dresses_skirts',
        #      'http://www.hm.com/il/products/ladies/blazers',
        #      'http://www.hm.com/il/products/ladies/tops',
        #      'http://www.hm.com/il/products/ladies/cardigans_jumpers',
        #      'http://www.hm.com/il/products/ladies/hoodies_sweatshirts',
        #      'http://www.hm.com/il/products/ladies/dresses',
        #      'http://www.hm.com/il/products/ladies/jumpsuits',
        #  ]
    }

def main():
    HMProduct.scrape_whole_brand(HM_CATEGORIES,'hm.json')

if __name__ == '__main__':
    main()