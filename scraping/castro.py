import json

import requests
from bs4 import BeautifulSoup
import dryscrape

from scraping.ScrapeProduct import ScrapeProduct
from scraping.utils import get_html_with_js, get_html
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count

class CastroProduct(ScrapeProduct):

    def __init__(self, url, gender):
        super().__init__(url)
        self.gender = gender

    def load_html(self):
        return get_html_with_js(self.url)

    def scrape_name(self):
        return self.soup.find('div', attrs={'class': 'name'}).find('h1').contents[0]

    def scrape_price(self):
        return self.soup.find('span', attrs={'class': 'price'}).next.next.next.strip() + "[NIS]"

    def scrape_sizes(self):
        sizes_anchors = self.soup.find('dd', attrs={'class': 'variants size-variants'}).findAll('a')
        return [a['title'] for a in sizes_anchors]

    def scrape_color(self):
        return self.soup.find('dd', attrs={'class': 'selected'}).contents[0]

    def scrape_description(self):
        description_div = self.soup.find('div', attrs={'class': 'attr-description'})
        desc = ""
        try:
            desc = description_div.next
            desc += "\n".join(li.contents[0] for li in description_div.find('ul').findAll('li'))
        except Exception:
            desc = description_div.contents
        return desc

    def scrape_imgs(self):
        return [a['rev'][0] for a in self.soup.findAll('a', attrs={'class': 'MagicThumb-swap'})]

    def scrape_brand(self):
        return "Castro"

    def scrape_gender(self):
        return self.gender

def scrape_castro_category(html, gender):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.findAll('a',attrs={'class':'product-image'})
    products = []
    for prod in data:
        print("product:", prod['href'])
        prod = CastroProduct(prod['href'], gender)
        products.append(prod)
        
    return products



def scrape_castro(save_path):
    categories = {
        'Male':[
            'https://www.castro.com/he/MEN/T-shirts.html',
            'https://www.castro.com/he/MEN/Jumpers.html',
            'https://www.castro.com/he/MEN/Knits.html',
            'https://www.castro.com/he/MEN/Coats.html',
            'https://www.castro.com/he/MEN/Shirts.html',
            'https://www.castro.com/he/MEN/Polo-Shirts.html',
            'https://www.castro.com/he/catalog/category/view/id/1820',
            'https://www.castro.com/he/MEN/Tank-tops.html',
        ],
        'Female':[
            'https://www.castro.com/he/WOMEN/Dresses.html',
            'https://www.castro.com/he/WOMEN/Tops.html',
            'https://www.castro.com/he/WOMEN/Knits.html',
            'https://www.castro.com/he/WOMEN/Jumpers.html',
            'https://www.castro.com/he/WOMEN/Blazers.html',
            'https://www.castro.com/he/WOMEN/Coats.html',
            'https://www.castro.com/he/WOMEN/Jumpsuits.html',
        ]
    }
    products = []
    # TODO: for some reason, returned html is not good when
    # there are more pending requests than #CPUs. fix this.
    N_THREADS = 1
    pool = Pool(N_THREADS)
    results = pool.starmap(scrape_castro_category, [(get_html(category_url), gender) for gender in categories.keys() for category_url in categories[gender]])
    print(results)
    scrapes = []
    for res in results:
        scrapes.extend(res)

    ScrapeProduct.json_from_scrapes(save_path, scrapes)


if __name__ == "__main__":
    scrape_castro('castro.json')

 