from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://www.sreality.cz/hledani/prodej/byty/brno?stari=mesic")
soup = BeautifulSoup(driver.page_source,"html.parser")
driver.quit()

for title in soup.select(".text-wrap"):
    num = "https://www.sreality.cz" + title.select_one(".title").get('href')
    print(num)