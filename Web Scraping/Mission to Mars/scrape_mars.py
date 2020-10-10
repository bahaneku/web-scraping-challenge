from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import pymongo
import time
from pymongo import MongoClient
import time

data={}
def headline():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)

    # KL: added a timer to give the browser some time to load
    time.sleep(1)
    # response=requests.get(news_url)
    html = browser.html
    soup = bs(html, "html.parser")
    
    headlines = soup.find("div", class_="list_text")

    header = headlines.find("div", class_="content_title").text
    header = headlines.find("a").text
    header = header.strip()

    paragraph = headlines.find("div", class_="article_teaser_body")
    # KL: headlines.find() will return only 1 item -> you cannot index (traverse) a single value with [0]
    # teaser = paragraph[0].text
    teaser=paragraph.text
    teaser = teaser.strip()

    data.update({"latest_news":header,"Teaser":teaser})

    # KL: could use a browser.quit() here to be consistent with your approach
    browser.quit()

def featured_image():   
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    fullimage_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(fullimage_url)
    browser.click_link_by_id("full_image")
    browser.click_link_by_partial_text("more info")

    fullimage_url_string="https://www.jpl.nasa.gov/"
    html=browser.html
    soup=bs(html, "html.parser")
    image=soup.find("figure", class_="lede").a["href"]
    featured_image_url=fullimage_url_string+image

    data.update({"featured_image_url":featured_image_url})


    browser.quit()

def facts():
    marsfacts_url="https://space-facts.com/mars/"
    fact_table=pd.read_html(marsfacts_url)
    mars_table = fact_table[0]
    mars_table_transposed = mars_table.transpose()

    mars_table_html=mars_table_transposed.to_html(index=False, header=False, classes=["table", "table-striped"])

    html_table_file = open("table.html", "w")
    html_table_file.write(mars_table_html)
    html_table_file.close()

    # print(mars_table_html)
    data.update({"mars_fact_table":mars_table_html})

def images():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)
    time.sleep(1)
    # KL: need to initiate a blank dictionary and a blank list
    links={}
    hemis_image_urls=[]

    hemis_url_string = 'https://astrogeology.usgs.gov'

    html = browser.html
    soup = bs(browser.html)
    hemis = soup.find_all('div', class_='item')
    for each_hemis in hemis:
        # KL: i think you're trying to add the link as a value to a dictionary key. you have an extra = and the .find('a') needs to be moved
        links[each_hemis.find('div', class_='description').find('a').text] = each_hemis.find('a').get('href')
        # links=[each_hemis.find('a').find('div', class_='description')].find('a') = each_hemis.find('a').get('href')
    print(links)
    
    for each_hemis in links:
        # KL: the links are currently short, e.g. https://astrogeology.usgs.gov/. it needs to have the base url attached before
        browser.visit(hemis_url_string+links[each_hemis])
        soup = bs(browser.html)
        # KL: needs to have go further into the node to find the href attribute of the ul->li->a
        link = soup.find(class_='downloads').find('ul').find('li').find('a').get('href')
        # KL: needs to initiate a blank dictionary if the desired output is 
        # [{
        # 'title': 'fdsafdsa', 
        # 'url': 'fdsafdsa'
        # }, {}]
        hemis_image_url={}
        hemis_image_url['title'] = each_hemis
        hemis_image_url['img_url'] = link
        hemis_image_urls.append(hemis_image_url)



        # executable_path = {'executable_path': 'chromedriver.exe'}
        # browser = Browser('chrome', **executable_path, headless=True)

        # hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        # browser.visit(hemis_url)
        # hemis_url_string = "https://astrogeology.usgs.gov/"
        # html = browser.html
        # soup = bs(html, "html.parser")

    # links = []


    # for result in soup.find_all("div", class_="item"):
    #     link = result.find("a", class_="itemLink product-item")["href"]
    #     link = hemis_url_string+link
    #     browser.visit(link)
    #     html = browser.html
    #     soup = bs(html, "html.parser")
    #     image = soup.find("img", class_="wide-image")["src"]
    #     image_source = hemis_url_string+image
    #     title = soup.find("h2", class_="title").text
    #     links.append({"title": title, "link": image_source})

    data.update({"hemis_images": hemis_image_urls})
    browser.quit()
    # return data
    

def scrape():
    # KL: i commented out each function when debugging
    headline()
    featured_image()
    facts()
    images()
    # KL: i used print(data) to debug
    print(data)
    return data
# print(scrape())
