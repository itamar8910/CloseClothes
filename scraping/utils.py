import requests
import click
from AdvancedHTMLParser import IndexedAdvancedHTMLParser


@click.command()
@click.argument("url")
def page_html(url):
    return (requests.get(url).text)


def document(url):
    parser = IndexedAdvancedHTMLParser()
    parser.parseStr(get_html(url))
    return parser


if __name__ == '__main__':
    page_html()
