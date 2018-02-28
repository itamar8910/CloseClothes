from ScrapeProduct import ScrapeProduct
import utils
import re
import unittest

class ZaraProduct(ScrapeProduct):

    def __init__(self,url,gender):
        super().__init__(url)
        self.gender = gender

    def scrape_name(self):
        return self.soup.find(attributes={'class': "product-name"}).get_text()

    def scrape_brand(self):
        return "Zara"

    def scrape_color(self):
        return self.soup.find(attributes={'class': "_colorName"}).get_text()

    def scrape_description(self):
        return self.soup.find(attributes={'class': "description"}).get_text()

    def scrape_imgs(self):
        all_images = self.soup.findAll(attrs={'class': "image-big _img-zoom"})
        good_images = [all_images[0], all_images[1], all_images[-1]] #the other pics aren't always full body and might be confusing
        return [image.src for image in good_images]

    def scrape_sizes(self):
        try:
            desc = self.scrape_description()
            match = re.search(r'SIZE (.+)', desc)
            return match.group(0)
        except:
            return "Unknown"
        
    def scrape_price(self):
        return self.soup.find(attrs={'class', "price _product-price"})

    def scrape_gender(self):
        return self.gender #set from init

    def load_html(self):
        return utils.get_html(self.url)

class TestZaraProduct(unittest.TestCase):
    def setUp(self):
        self.product = ZaraProduct("https://www.zara.com/il/en/relaxed-basic-t-shirt-p01887440.html?v1=5517107&v2=1024006","male")
        self.expected = {
            "name":"RELAXED BASIC T-SHIRT",
            "price":"39.90 ILS",
            "description": """Basic cotton T-shirt with a straight fit, round neckline and short sleeves.\n\n HEIGHT OF MODEL: 189 cm. / 6′ 2″ SIZE L""",
            "gender":"male",
            "imgs": ["https://static.zara.net/photos///2018/V/0/2/p/5857/450/800/2/w/1024/5857450800_1_1_1.jpg?ts=1514890659316", "https://static.zara.net/photos///2018/V/0/2/p/5857/450/800/2/w/560/5857450800_2_1_1.jpg?ts=1514890636709", "https://static.zara.net/photos///2018/V/0/2/p/5857/450/800/2/w/1024/5857450800_6_1_1.jpg?ts=1516797252962"]
        }
        
    def test_properties(self):
        for key,value in self.product.properties():
            self.assertEqual(value, self.expected[key], msg="""Property {key} test failed.
            expected {key}:{expected}
             actual {key}:{value}""".format(
                key=key, expected=self.expected[key], value=value))

if __name__ == '__main__':
    unittest.main()