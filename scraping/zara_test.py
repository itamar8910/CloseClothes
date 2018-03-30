from zara import ZaraProduct
import unittest
class TestZaraProduct(unittest.TestCase):
    def setUp(self):
        self.product = ZaraProduct("https://www.zara.com/il/en/relaxed-basic-t-shirt-p04834460.html?v1=5981525&v2=374004","male")
        self.expected = {
            "url":"https://www.zara.com/il/en/relaxed-basic-t-shirt-p04834460.html?v1=5981525&v2=374004",
            "name":"RELAXED BASIC T-SHIRT",
            "price":"",
            "description": """Basic cotton T-shirt with a straight fit, round neckline and short sleeves.HEIGHT OF MODEL: 189 cm. / 6′ 2″ SIZE L""",
            "gender":"male",
            "color":"white",
            "brand":"zara",
            "sizes":["L"],
            "imgs": ["https://static.zara.net/photos///2018/V/0/2/p/5857/450/800/2/w/1024/5857450800_1_1_1.jpg?ts=1514890659316", "https://static.zara.net/photos///2018/V/0/2/p/5857/450/800/2/w/560/5857450800_2_1_1.jpg?ts=1514890636709", "https://static.zara.net/photos///2018/V/0/2/p/5857/450/800/2/w/1024/5857450800_6_1_1.jpg?ts=1516797252962"]
        }
        
    def test_properties(self):
        for key,value in self.product.properties().items():
            try:
                value = value.lower()
                self.expected[key] = self.expected[key].lower()
            except AttributeError:
                pass
            finally:
                self.assertEqual(value, self.expected[key], msg="""Property {key} test failed.
                expected {key}:{expected}
                actual {key}:{value}""".format(
                    key=key, expected=self.expected[key], value=value))

if __name__ == '__main__':
    unittest.main()