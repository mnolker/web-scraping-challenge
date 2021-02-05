from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from flask import Flask, render_template
from flask_pymongo import PyMongo

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
    results = soup.find('ul', class_='item_list')
    results_title = results.find('li', class_='slide')
    top_news = results_title.find('div', class_='bottom_gradient')
    top_news_title = top_news.find('h3').text
    top_news_p = results.find('div',class_='rollover_description_inner').text

    # add news title & p to mars_data dictionary
    mars_data["news_title"] = top_news_title
    mars_data["news_paragraph"] = top_news_p
    

    # visit url & gather facts on Mars from table
    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)
    soup = BeautifulSoup(html, 'html.parser')
    
    tables = pd.read_html(url_facts)
    mars_table = tables[0]
    mars_table.columns = ['fact', 'Mars_value']
    mars_table = mars_table.set_index('fact')
    mars_table_html = mars_table.to_html(classes='mars_facts_table')

    # add it to our mars_data dict
    mars_data["facts"] = mars_table_html

    # scrape hemispheres using splinter to navigate to full size image
    url_hemipheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemipheres)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    links = browser.find_by_css("a.itemLink.product-item h3")

    hemisphere_image_urls = []

    for result in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.itemLink.product-item h3")[result].click()
        sample = browser.find_by_text("Sample").first
        img_url = sample["href"]
        img_title = browser.find_by_css("h2.title").text
    
        hemisphere['img_url'] = img_url
        hemisphere['title'] = img_title
        hemisphere_image_urls.append(hemisphere)
    
        browser.back()
    
    # add it to our mars_data dict
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()
    
    print(mars_data)
    return mars_data

