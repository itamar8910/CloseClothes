import requests
import click
from AdvancedHTMLParser import IndexedAdvancedHTMLParser
import dryscrape

@click.command()
@click.argument("url")
def page_html(url):
    return (requests.get(url).text)

def get_html_with_js(url):
    session = dryscrape.Session()
    session.visit(url)
    return session.body()

def document(url):
    parser = IndexedAdvancedHTMLParser()
    parser.parseStr(get_html(url))
    return parser


if __name__ == '__main__':
    page_html()
