import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import re
from webdriver_manager.chrome import ChromeDriverManager


def scrape():

    #create an executable path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_news = {}
    
    #scrape for the url
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #use beautiful soup to pull refer to the website
    html=browser.html
    soup=bs(html, 'html.parser')

    latest_news = soup.find_all('div', class_='content_title')

    #save the title
    news_title = latest_news[0].text
    mars_news['title'] = news_title

    latest_p = soup.find('div', class_='article_teaser_body')
    
    #save the paragraph
    news_p = latest_p.text
    mars_news['paragraph'] = news_p

    # ## Space Images

    #create image path
    im_url = 'https://spaceimages-mars.com/'
    # space_imgage_url = 'img'
    browser.visit(im_url)

    #use beauriful soup to access the website
    img_html = browser.html
    soup = bs(img_html, 'html.parser')


    image = soup.find('img', class_ = 'headerimage fade-in')

    image_url = image["src"]
    image_url


    featured_image_url = f'{im_url}{image_url}'
    mars_news['featured_img_url'] = featured_image_url


    # ## Mars Facts


    facts_url = 'https://galaxyfacts-mars.com'

    tables= pd.read_html(facts_url)
    tables

    mars_facts = tables[1]
    mars_facts.columns = ["Description", "Mars"]
    mars_facts


    mars_facts_html = mars_facts.to_html()
    mars_facts_html

    mars_facts_html = mars_facts_html.replace('\n','')

    mars_news['table'] = mars_facts_html


    # ## Mars Hemispheres


    hemi_url = 'https://marshemispheres.com/'
    image_url_link = 'https://marshemispheres.com/images/'
    browser.visit(hemi_url)

    hemi_html = browser.html

    soup = bs(hemi_html, 'html.parser')


    results = soup.find_all('div', class_ = 'description')

    list_hemi = []
    for i in range(len(results)):
        list_hemi.append(results[i].a.h3.text)

    list_hemi

    html_links = []
    for row in results:
        html_links.append(hemi_url + (row.find('a', class_='itemLink product-item')['href']))

    html_links

    hemisphere_url = []

    for url in html_links:
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2', class_='title').text
        img_url = hemi_url + soup.find('img', class_="wide-image")['src']
        results_new = soup.find_all('li')
        hemisphere_url.append({"title":title, "img_url":img_url})
    mars_news["hemisphere"] = hemisphere_url  

    browser.quit()


    return mars_news


