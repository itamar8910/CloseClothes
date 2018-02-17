import requests
import click
from AdvancedHTMLParser import IndexedAdvancedHTMLParser
import dryscrape
import time
@click.command()
@click.argument("url")
def page_html_cmd(url):
    return (requests.get(url).text)


def get_html(url):
    return (requests.get(url).text)

def get_html_with_js(url):
    t1 = time.time()
    session = dryscrape.Session()
    session.set_attribute('auto_load_images', False)
    session.visit(url)
    print(time.time() - t1)
    return session.body()

def document(url):
    parser = IndexedAdvancedHTMLParser()
    parser.parseStr(get_html(url))
    return parser


if __name__ == '__main__':
    page_html_cmd()
