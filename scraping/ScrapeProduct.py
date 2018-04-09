from abc import ABC, abstractproperty, abstractmethod
import json
from bs4 import BeautifulSoup
import utils


class ScrapeProduct(ABC):
    def __init__(self, url):
        self.url = url
        self.name = None
        self.brand = None
        self.color = None
        self.description = None
        self.imgs = None
        self.price = None
        self.sizes = None
        self.gender = None
        self.soup = None
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

    def properties(self):
        all_vars = vars(self)
        all_vars.pop('soup')
        return all_vars

    def to_json(self):
        return json.dumps(self.properties())


    @staticmethod
    def json_from_scrapes(path, scrapes):
        with open(path, 'w') as fp:
            json_str = json.dumps([scrape.properties() for scrape in scrapes], indent=2)
            fp.write(json_str)


    def __str__(self):
        return str(self.to_json())