import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    #print(url)
    html = requests.Session().get(url).text
    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    category = soup.find('img', {'class':'product-flag-overlay'})
    print(len(category))
    

if __name__ == "__main__":
    scrape_page('https://www.castro.com/he/MEN/Jumpers.html')
    # pages = ['http://www.hm.com/il/products/men/hoodies_sweatshirt', 'http://www.hm.com/il/department/MEN']
    # for page in pages:
    #     scrape_page(page)
    #     break



    # url = 'http://www.hm.com/il/products/men/hoodies_sweatshirt'
    # headers = header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}

    # response = requests.get(url, headers=headers)
    # print(response.text)