import json

import requests
from bs4 import BeautifulSoup
import dryscrape

from ScrapeProduct import ScrapeProduct
from utils import get_html_selenium, get_html
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count
import pickle
from utils import get_html_selenium

N_PRODUCTS = 0
N_SCRAPED = 0

# TODO: H&M products have multiple color versions, this onyl scrapes the default one
class HMProduct(ScrapeProduct):
    def __init__(self, url, gender):
        super().__init__(url)
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
#
#
# def scrape_castro_category(html, gender, category_url="N/A"):
#     global N_PRODUCTS, N_SCRAPED
#     print("starting category:", category_url)
#     soup = BeautifulSoup(html, 'html.parser')
#     data = soup.findAll('a', attrs={'class': 'product-image'})
#     N_PRODUCTS += len(list(data))
#     products = []
#     for prod_i, prod in enumerate(data):
#         print("product:", prod['href'], "{}/{}".format(N_SCRAPED, N_PRODUCTS))
#         N_SCRAPED += 1
#         prod = CastroProduct(prod['href'], gender)
#         products.append(prod)
#
#     print("Finished category:", category_url)
#     return products
#
#
# def scrape_castro(save_path):
#     categories = {
#         'Male': [
#             'https://www.castro.com/he/MEN/T-shirts.html',
#             'https://www.castro.com/he/MEN/Jumpers.html',
#             'https://www.castro.com/he/MEN/Knits.html',
#             'https://www.castro.com/he/MEN/Coats.html',
#             'https://www.castro.com/he/MEN/Shirts.html',
#             'https://www.castro.com/he/MEN/Polo-Shirts.html',
#             'https://www.castro.com/he/catalog/category/view/id/1820',
#             'https://www.castro.com/he/MEN/Tank-tops.html',
#         ],
#         'Female': [
#             'https://www.castro.com/he/WOMEN/Dresses.html',
#             'https://www.castro.com/he/WOMEN/Tops.html',
#             'https://www.castro.com/he/WOMEN/Knits.html',
#             'https://www.castro.com/he/WOMEN/Jumpers.html',
#             'https://www.castro.com/he/WOMEN/Blazers.html',
#             'https://www.castro.com/he/WOMEN/Coats.html',
#             'https://www.castro.com/he/WOMEN/Jumpsuits.html',
#         ]
#     }
#     products = []
#     N_THREADS = 8
#     pool = Pool(N_THREADS)
#     results = pool.starmap(scrape_castro_category,
#                            [(get_html(category_url), gender, category_url) for gender in categories.keys() for
#                             category_url in categories[gender]])
#     print(results)
#     scrapes = []
#     for res in results:
#         scrapes.extend(res)
#     # with open('castro_save.p', 'wb') as f:
#     #     pickle.dump(scrapes, f)
#     ScrapeProduct.json_from_scrapes(save_path, scrapes)


if __name__ == "__main__":
    # print(HMProduct('http://www.hm.com/il/product/83134?article=83134-A', 'male'))
    print(HMProduct('http://www.hm.com/il/product/96562?article=96562-E', 'male'))
    # print(HMProduct('http://www.hm.com/il/product/00566?article=00566-B', 'male'))
