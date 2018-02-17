from abc import ABC, abstractproperty, abstractmethod
import json
from bs4 import BeautifulSoup
import utils


class ScrapeProduct(ABC):
    def __init__(self, url):
        self.url = url
        self._name = None
        self._brand = None
        self._color = None
        self._description = None
        self._imgs = None
        self._price = None
        self._sizes = None
        self._gender = None
        self.scrape()

    def url(self):
        return self.url

    @abstractmethod
    def load_html(self):
        "returns html of product url"
        # This may by implemented by either requests or dryscrape,
        # so better leave the decision to the children
        pass

    def scrape(self):
        "scrapes prodcut page and sets properties"
        # set up the soup object for the child
        self.soup = BeautifulSoup(self.load_html(), 'html.parser')

        self.name = self.scrape_name()
        self.brand = self.scrape_brand()
        self.color = self.scrape_color()
        self.description = self.scrape_description()
        self.imgs = self.scrape_imgs()
        self.price = self.scrape_price()
        self.sizes = self.scrape_sizes()
        self.gender = self.scrape_gender()

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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, val):
        self._brand = val

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, val):
        self._price = val

    @property
    def sizes(self):
        return self._sizes

    @sizes.setter
    def sizes(self, val):
        self._sizes = val


    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val


    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val

    @property
    def imgs(self):
        return self._imgs
    @imgs.setter
    def imgs(self, val):
        self._imgs = val

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, val):
        self._gender = val

    def properties(self):
        all_vars = vars(self)
        all_vars.pop('soup', None)
        return all_vars

    def to_json(self):
        return json.dumps(self.properties())

    @staticmethod
    def json_from_scrapes(path, scrapes):
        with open(path, 'w') as fp:
            json.dump(fp, [scrape.to_json() for scrape in scrapes])


