from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/windows/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # create surf_data dict that we can insert into mongo
    mars_data = {}

    # visit NASA Mars News
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    html = browser.html

    # create a soup object from the html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('li', class_='slide')

    top_news = results.find('div', class_='content_title').text
    top_news_p = results.find('div', class_='article_teaser_body').text

    # add news title & p to mars_data dictionary
    mars_data["news_title"] = top_news
    mars_data["news_paragraph"] = top_news_p

    #visit url & gather facts on Mars from table
    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)
    soup = BeautifulSoup(html, 'html.parser')
    
    tables = pd.read_html(url)
    mars_data = tables[0]
    df.columns = ['fact', 'Mars_value']
    df = df.set_index('fact')
    mars_table_html = df.to_html(classes='mars_facts_table')

    # add it to our mars_data dict
    mars_data["facts"] = build_report(mars_data)

    browser.quit()
    return mars_data

