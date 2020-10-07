from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import pymongo
import time
from pymongo import MongoClient

data={}
def headline():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)

    # response=requests.get(news_url)
    html = browser.html
    soup = bs(html, "html.parser")

    headlines = soup.find("div", class_="list_text")

    header = headlines.find("div", class_="content_title").text
    header = headlines.find("a").text
    header = header.strip()

    paragraph = headlines.find("div", class_="article_teaser_body")
    teaser = paragraph[0].text
    teaser = teaser.strip()

    data.update({"latest_news":header,"Teaser":teaser})

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

    data.update({"featured_image":featured_image_url})


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

    data.update({"mars_fact_table":mars_table_html})

# def images():
#     executable_path = {'executable_path': 'chromedriver.exe'}
#     browser = Browser('chrome', **executable_path, headless=False)
    
#     hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#     browser.visit(hemis_url)
#     time.sleep(1)

#     hemis_url_string = 'https://astrogeology.usgs.gov/'

#     html = browser.html
#     soup = bs(browser.html)
#     hemis = soup.find_all('div', class_='item')
#     for each_hemis in hemis:
#         links=[each_hemis.find('a').find('div', class_='description')].find('a') = each_hemis.find('a').get('href')
#     for each_hemis in links:
#         browser.visit(links[each_hemis])
#         soup = bs(browser.html)
#         link = soup.find(class_='downloads').find('ul').find
#         hemis_image_urls['title'] = each_hemis

#         executable_path = {'executable_path': 'chromedriver.exe'}
#         browser = Browser('chrome', **executable_path, headless=True)

#         hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
#         browser.visit(hemis_url)
#         hemis_url_string = "https://astrogeology.usgs.gov/"
#         html = browser.html
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

    browser.quit()

    data.update({"hemis_images": hemis_image_urls})
    return data
    

def scrape():
    headline()
    featured_image()
    facts()
    images()
    print(headline())
    return data
print(scrape())
