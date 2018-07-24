import requests
import time
from bs4 import BeautifulSoup
import os
from os import path
from selenium import webdriver
import warnings
def get_html(url):
    return (requests.get(url).text)

def get_html_selenium(url, verbose = False):
    """downloads the html from `url` using selenium and phantomjs"""
    t1 = time.time()
    if verbose:
        print("scraping:", url)
    # add phantomjs driver to path
    # TODO: extract this logic to a singleton (but we want a separate instance for each thread...)
    scraping_dir_path = path.dirname(path.abspath(__file__))
    os.environ["PATH"] += os.pathsep + path.join(scraping_dir_path, "phantomjs")

    # we're supressing the following warning:
    # UserWarning: Selenium support for PhantomJS has been deprecated,
    # please use headless versions of Chrome or Firefox instead
    with warnings.catch_warnings():

        warnings.simplefilter('ignore')
        driver = webdriver.PhantomJS()

    driver.get(url)
    print("Scrape time:{0:.2f}".format(time.time() -t1))
    return driver.page_source

if __name__ == "__main__":
    print(get_html_selenium('https://www.castro.com/he/MEN/Jackets/Navy-tailored-jacket-313596.html', verbose=True))
