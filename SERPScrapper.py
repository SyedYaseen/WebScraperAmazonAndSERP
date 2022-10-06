import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium import webdriver
from webdrivermanager.chrome import ChromeDriverManager
import pandas as pd
from selenium.common.exceptions import ElementClickInterceptedException



def get_source(url):
    """Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


# Headless
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
Service = Service('chromedriver_win32/chromedriver.exe')

target_links =[] #List for GetLinksMethod

def GetHeadlessSoup(URL):

    driver = webdriver.Chrome(options=options, service=Service)
    driver.get(URL)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, "lxml")
    driver.quit()
    return soup


def scrape_google(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.',
                      'https://google.',
                      'https://webcache.googleusercontent.',
                      'http://webcache.googleusercontent.',
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
    return links


def get_links(keywordList):
    try:
        listSize = len(keywordList)
        chunked_list = list()
        chunk_size = 20
        for i in range(0, listSize, chunk_size):
            chunked_list.append(keywordList[i:i + chunk_size])
        print(chunked_list)

        for kw in keywordList:
            links_list = scrape_google(kw)
            print("")
            print(kw)

            for link in links_list:
                print(link)
                soup = GetHeadlessSoup(link)

                if soup:
                    sources = soup.findAll('script', {"src": True})
                    if sources:
                        for source in sources:
                            if "doubleclick" in source['src']:
                                target_links.append([kw,link])
                                break
        print(target_links)
        return target_links

    finally:
        SaveToCSV()
        print("BackUpSaved")



def SaveToCSV():
    # pd.DataFrame(target_links).to_csv("targetLinksBackup.csv")
    pd.DataFrame(target_links).to_csv("targetLinksBackup.csv", mode='a', index=True, header=False)


def execute():
    Keywordsdf = pd.read_csv('Keywords2.csv')
    keywords = Keywordsdf["Keyword"].values.tolist()

    #break into chunks
    listSize = len(keywords)
    chunked_list = []
    chunk_size = 20
    for i in range(0, listSize, chunk_size):
        chunked_list.append(keywords[i:i + chunk_size])

    for list in chunked_list:
        LinksList = get_links(list)
    # pd.DataFrame(LinksList).to_csv("targetLinks.csv")
    print("Done")

execute()


