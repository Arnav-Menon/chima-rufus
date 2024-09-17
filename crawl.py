# from bs4 import BeautifulSoup
# import requests

# def simple_crawl(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     return soup

from selenium import webdriver

def selenium_crawl(url):
    driver = webdriver.Chrome()
    driver.get(url)
    page = driver.page_source
    driver.quit()
    return page
