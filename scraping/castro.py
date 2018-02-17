import requests
from bs4 import BeautifulSoup
import dryscrape

from scraping.ScrapeProduct import ScrapeProduct
from scraping.utils import get_html_with_js

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
        desc = description_div.next
        desc += "\n".join(li.contents[0] for li in description_div.find('ul').findAll('li'))
        return desc

    def scrape_imgs(self):
        return [a['rev'][0] for a in self.soup.findAll('a', attrs={'class': 'MagicThumb-swap'})]

    def scrape_brand(self):
        return "Castro"

    def scrape_gender(self):
        return self.gender



def get_html(url):
    return (requests.get(url).text)



def get_prod_data(prod_html):
    pass
    

def scrape_castro(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.findAll('a',attrs={'class':'product-image'})
    for prod in data:
        print("product:", prod['href'])
        prod = CastroProduct(prod['href'], 'Male')
        print(prod.to_json())
        exit()

if __name__ == "__main__":
    html = get_html('https://www.castro.com/he/MEN/Jumpers.html')
    scrape_castro(html)
    # with open('scraping/prod_html.html', 'r') as f:
    #     get_prod_data(f.read())
 