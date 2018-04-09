from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count
from typing import Dict

from scraping.ScrapeProduct import ScrapeProduct
from scraping.utils import get_html_selenium
from scraping.hm import scrape_hm_category, HM_CATEGORIES


def scrape(scrape_category_func, categories_urls : Dict, scarpe_json_dst, N_THREADS = 8):
    """
    runs the scraping process

    :param scrape_category_func: function that gets a category and returns it's ScrapeProducts
    :param categories_urls: urls of categories to scrape. It's a dict with structure: <gender> -> <list of urls>
    :param scarpe_json_dst: destination path for resulting json
    :param N_THREADS: number of threads to use in the scraping process
    :return:
    """

    pool = Pool(N_THREADS)
    print("STARTED")
    results = pool.starmap(scrape_category_func,
                           [(get_html_selenium(category_url), gender, category_url) for gender in categories_urls.keys() for
                            category_url in categories_urls[gender]])
    print(results)
    scrapes = []
    for res in results:
        scrapes.extend(res)

    ScrapeProduct.json_from_scrapes(scarpe_json_dst, scrapes)

if __name__ == "__main__":
    scrape(scrape_hm_category, HM_CATEGORIES, 'hm.json')