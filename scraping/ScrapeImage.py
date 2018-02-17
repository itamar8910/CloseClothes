from abc import ABC, abstractproperty, abstractmethod
from AdvancedHTMLParser import IndexedAdvancedHTMLParser
import json
import utils


class ScrapeImage(ABC):
    def __init__(self,url):
        self.document = utils.document(url)
        self.url = url

    def url(self):
        return self.url
    
    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def brand(self):
        pass

    @abstractproperty
    def name(self):
        pass

        

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def price(self):
        pass

    @abstractproperty
    def sizes(self):
        pass

    @abstractproperty
    def description(self):
        pass

    @abstractproperty
    def color(self):
        pass

    def properties(self):
        return {prop:getattr(self,prop) for prop in dir(self) if not callable(getattr(self,prop))}

    @staticmethod
    def json_from_scrapes(name, scrapes):
        with open(name,'w') as fp:
            json.dump(fp, [scrape.prop for scrape in args])

