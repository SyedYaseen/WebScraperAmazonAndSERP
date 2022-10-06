import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium import webdriver
from webdrivermanager.chrome import ChromeDriverManager
import pandas as pd
import requests
from selenium.common.exceptions import ElementClickInterceptedException

# Headless
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# Using Regular Browser
Service = Service('chromedriver_win32/chromedriver.exe')

# Get headless Soup
def GetHeadlessSoup(URL):
    driver = webdriver.Chrome(options=options, service=Service)
    driver.get(URL)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, 'lxml')
    # print(soup)
    driver.quit()
    return soup

def GetReviews(soup):

    reviewsFromSoup = soup.find_all('div', {'data-hook':'review'})
    # print(reviewsFromSoup)
    return reviewsFromSoup

#Get Reviews
reviewsList = []
for n in range(1, 68):
    URL = f'https://www.amazon.com/Everlywell-Food-Sensitivity-Test-CLIA-Certified/product-reviews/B085648CRJ/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber={n}'
    soup = GetHeadlessSoup(URL)
    last_page = soup.findAll('li', {'class':'a-disabled a-last'})

    reviewsSoup = GetReviews(soup)
    for item in reviewsSoup:
        review= {
            'Title': item.find('a', {'data-hook':'review-title'}).text.strip(),
            'Rating': float(item.find('i', {'data-hook':'review-star-rating'}).text.replace(' out of 5 stars','')),
            'Review': item.find('span', {'data-hook':'review-body'}).text.strip()
        }

        reviewsList.append(review)

    print(f'Page Number: {n}')
    print(len(reviewsList))

    if last_page:
        break
    else:
        pass

Reviewdf = pd.DataFrame(reviewsList)
print(Reviewdf)
Reviewdf.to_csv('Everylwell-Reviews2.csv', index=False)
print("Done")
