from algorithm.scraping.ScrapeProduct import ScrapeProduct
import algorithm.scraping.utils
import re

class ZaraProduct(ScrapeProduct):

    def __init__(self,url,gender):
        super().__init__(url)
        self.gender = gender

    def scrape_name(self):
        return self.soup.find(class_="product-name").string

    def scrape_brand(self):
        return "Zara"

    def scrape_color(self):
        return self.soup.find(class_="_colorName").get_text()

    def scrape_description(self):
        return self.soup.find(class_="description").get_text()

    def scrape_imgs(self):
        all_images = self.soup.findAll(class_="_seoImg")
        good_images = [all_images[0], all_images[1], all_images[-1]] #the other pics aren't always full body and might be confusing
        return [image.href for image in good_images]

    def scrape_sizes(self):
        try:
            desc = self.scrape_description()
            match = re.search(r'SIZE (.+)', desc)
            return [match.group(1)]
        except:
            return "Unknown"
        
    def scrape_price(self):
        return None

    def scrape_gender(self):
        return self.gender #set from init

    def load_html(self):
        return utils.get_html_with_js(self.url)
