#Import the necessary libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
#import time

# Get header for scrapping
HEADERS = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/90.0.4430.212 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})

# Scrap reviews from product websites
def get_reviews(product_url):
    url_parse = urlparse(product_url)
    domain = f"{url_parse.scheme}://{url_parse.netloc}"
    product_page = requests.get(product_url, headers=HEADERS)
    page_html = BeautifulSoup(product_page.content, 'html.parser')
    pagination_div = page_html.find(id="cr-pagination-footer-0")
    review_link = pagination_div.find("a")
    link = review_link['href']
    review_count = 0
    page_number = 1
    review_array = list()
    while review_count <= 550  and page_number < 100:
        #time.sleep(3)
        review_url = f"{domain}{link}&pageNumber={page_number}"
        review_page = requests.get(review_url, headers=HEADERS)
        review_html = BeautifulSoup(review_page.content, 'html.parser')
        reviews = review_html.select('span[data-hook="review-body"]')
        for review in reviews:
            review_array.append(review.get_text().replace("\n"," "))
            review_count = review_count + 1
        page_number = page_number + 1
    return review_array

#url1 = "https://www.amazon.com/AmazonBasics-LR03-36PK-Parent-Performance-Alkaline-Batteries/dp/B07NVTGRVZ/ref=cm_cr_arp_d_product_top?ie=UTF8&th=1"
#url2 = "https://www.amazon.com/Samsung-Factory-Unlocked-Smartphone-Pro-Grade/dp/B08FYVHB8Z/ref=sr_1_3?crid=31O2ZGKD3XKTY&keywords=phone&qid=1647989360&sprefix=phone%2Caps%2C282&sr=8-3"
#url3 = "https://www.amazon.com/Stronger-Together-Blueprint-Americas-Future/dp/1501161733/"
#url4 = "https://www.amazon.de/-/en/America-Donald-Unisex-Adjustable-Keep-red/dp/B07K4F8GH5/ref=sr_1_3?keywords=trump%2Bmake%2Bamerica%2Bgreat%2Bagain%2Bred%2Bcap%2Bsammlerst%C3%BCck&linkCode=gs3&qid=1648157241&sr=8-3&th=1"
#reviews = get_reviews(url4)
#print(len(reviews))
#print(reviews)
