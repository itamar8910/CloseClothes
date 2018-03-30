import requests
try:
    import dryscrape
except ImportError:
    print("Dryscrape not installed") #for work on windows
import time
from bs4 import BeautifulSoup

def get_html(url):
    return (requests.get(url).text)

def get_html_with_js(url):
    t1 = time.time()
    session = dryscrape.Session()
    session.set_attribute('auto_load_images', False)
    session.visit(url)
    print(time.time() - t1)
    return session.body()
