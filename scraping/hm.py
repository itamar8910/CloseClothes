import json

import requests
from bs4 import BeautifulSoup
import dryscrape

from ScrapeProduct import ScrapeProduct
from utils import get_html_selenium, get_html

import pickle
from utils import get_html_selenium

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

def get_all_color_variants_url_of_product(prod_soup, prod_url):
    prod_base_url = prod_url[:prod_url.index('?article=')]
    return [prod_base_url + color_prod.find('a')['href'] for color_prod in prod_soup.find('ul', attrs={'id':'options-articles'}).findAll('li')]


def irrelevant_product(prod : HMProduct) -> bool:
    bad_names = ["trouses", "socks", "thong", "pants"]
    return any([x in prod.name.lower() for x in bad_names])


def scrape_hm_category(html, gender, category_url="N/A"):
    global N_PRODUCTS, N_SCRAPED
    print("starting category:", category_url)
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.findAll('a', attrs={'class': 'product-url js-product-tracking js-product-tracking-initialized'})
    products = []
    for prod_box in data:
        print(prod_box['href'])
        prod_soup = BeautifulSoup(get_html_selenium(prod_box['href']), 'html.parser')
        prod_colors_urls = get_all_color_variants_url_of_product(prod_soup, prod_box['href'])
        print("color variants:", prod_colors_urls)
        for prod_color_url in prod_colors_urls:
            products.append(
                {'url': prod_color_url,
                 'soup': prod_soup if prod_color_url != prod_box['href'] else None}
            )
    print("# of items:", len(products))

    N_PRODUCTS += len(list(products))
    products = []
    for prod_i, prod in enumerate(products):
        print("product:", prod['url'], "{}/{}".format(N_SCRAPED, N_PRODUCTS))
        prod_soup = prod['soup'] if prod['soup'] else BeautifulSoup(get_html_selenium(prod['url']), 'html.parser')
        N_SCRAPED += 1
        prod = HMProduct(prod['href'], gender, soup=prod_soup)
        if not irrelevant_product(prod):
            products.append(prod)

    print("Finished category:", category_url)
    return products

HM_CATEGORIES = {
        'Male': [
            "http://www.hm.com/il/products/men/jumpers_cardigans",
            "http://www.hm.com/il/products/men/outerwear",
            "http://www.hm.com/il/products/men/shirts",
            "http://www.hm.com/il/products/men/tshirt",
            "http://www.hm.com/il/products/men/blazers_suits",
            "http://www.hm.com/il/products/men/hoodies_sweatshirt"
        ],
        'Female': [
            'http://www.hm.com/il/products/ladies/basics/tops',
            'http://www.hm.com/il/products/ladies/basics/cardigansjumpers',
            'http://www.hm.com/il/products/ladies/basics/dresses_skirts',
            'http://www.hm.com/il/products/ladies/blazers',
            'http://www.hm.com/il/products/ladies/tops',
            'http://www.hm.com/il/products/ladies/cardigans_jumpers',
            'http://www.hm.com/il/products/ladies/hoodies_sweatshirts',
            'http://www.hm.com/il/products/ladies/dresses',
            'http://www.hm.com/il/products/ladies/jumpsuits',
        ]
    }

