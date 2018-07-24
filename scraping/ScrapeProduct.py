from abc import ABC, abstractproperty, abstractmethod
import json
from bs4 import BeautifulSoup
import utils
import concurrent.futures
from functools import partial

class ScrapeProduct(ABC):
    """Abstract base class of a scraper. Implements the downloading and orginizing where it's derivitives implement analyzing the HTML"""
    def __init__(self, url, soup = None):
        self.url = url
        self.name = None
        self.brand = None
        self.color = None
        self.description = None
        self.imgs = None
        self.price = None
        self.sizes = None
        self.gender = None
        self.soup = soup
        self.scrape()

    @abstractmethod
    def load_html(self):
        "returns html of product url"
        # This may be implemented by either requests or dryscrape,
        # so better leave the decision to the children
        pass

    def scrape(self):
        "scrapes prodcut page and sets properties"
        # set up the soup object for the child
        N_RETRIES = 3
        success = False
        for i in range(N_RETRIES):
            try:
                if self.soup is None:
                    self.soup = BeautifulSoup(self.load_html(), 'html.parser')
                self.name = self.scrape_name()
                self.brand = self.scrape_brand()
                self.color = self.scrape_color()
                self.description = self.scrape_description()
                self.imgs = self.scrape_imgs()
                self.price = self.scrape_price()
                self.sizes = self.scrape_sizes()
                self.gender = self.scrape_gender()
                success = True
                break
            except Exception as e:
                print(e)
                print("bad HTML, # retries: {} / {}".format(i+1, N_RETRIES))
                #print(self.soup.text)
                #raise e
        if not success:
            print("SCRAPE BAD, url:", self.url)
        else:
            print("SCRAPE GOOD")

    @abstractmethod
    def scrape_name(self):
        pass

    @abstractmethod
    def scrape_brand(self):
        pass

    @abstractmethod
    def scrape_color(self):
        pass

    @abstractmethod
    def scrape_description(self):
        pass

    @abstractmethod
    def scrape_imgs(self):
        pass

    @abstractmethod
    def scrape_sizes(self):
        pass

    @abstractmethod
    def scrape_price(self):
        pass

    @abstractmethod
    def scrape_gender(self):
        pass

    @staticmethod
    @abstractmethod
    def scrape_product_urls(category_url):
        pass

    @classmethod
    def scrape_category(cls,category_url,gender):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            category_html = utils.get_html_selenium(category_url)
            product_urls = cls.scrape_product_urls(category_html)
            products = [product for product in executor.map(lambda url:cls(url,gender),product_urls)] #have to iterate over executor.map while inside the "with" scope
        return products


    def properties(self):
        return {key:value for key,value in vars(self).items() if key != 'soup'}

    def to_json(self):
        return json.dumps(self.properties())


    @staticmethod
    def json_from_scrapes(path, scrapes):
        with open(path, 'w') as fp:
            json_str = json.dumps([scrape.properties() for scrape in scrapes], indent=2)
            fp.write(json_str)


    def __str__(self):
        return str(self.to_json())
    
    def __repr__(self):
        return str(self.to_json())

    @classmethod
    def scrape_whole_brand(cls,category_url_dict_by_gender,save_path):
        """ 

        scrape all of the brand  


        :param cls: given  
        :param category_url_dict_by_gender: dict of shape {gender:category_urls}
        :param save_path: path to save json in
        """
        #category_url_dict_by_gender = ['men':]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for gender,category_url_list in category_url_dict_by_gender.items():
                flattened_scrapes  = list()
                for scrape in executor.map(lambda category_url:cls.scrape_category(gender=gender,category_url=category_url),category_url_list):
                    flattened_scrapes.extend(scrape)

        ScrapeProduct.json_from_scrapes(save_path,flattened_scrapes) 
