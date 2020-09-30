from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import pymongo
import time
from pymongo import MongoClient

def scrape():
    # data = {}
# def headline(): 
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    response=requests.get(news_url)
    soup = bs(response.text, "lxml")

    headlines = soup.find_all("div", class_="list_text")

    header = headlines.find_all("div",class_="content_title")
    header = headlines[0].text
    header = header.strip()

    paragraph=headlines.find("div", class_="article_teaser_body")
    teaser = paragraph[0].text
    teaser = teaser.strip()

    # data.update({"latest_news":header,"Teaser":teaser})

# def featured_image():   
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

    # data.update({"featured_image":featured_image_url})


    browser.quit()

# def facts():
    marsfacts_url="https://space-facts.com/mars/"
    fact_table=pd.read_html(marsfacts_url)
    mars_table = fact_table[0]
    mars_table_transposed = mars_table.transpose()

    mars_table_html=mars_table_transposed.to_html(index=False, header=False, classes=["table", "table-striped"])

    html_table_file = open("table.html", "w")
    html_table_file.write(mars_table_html)
    html_table_file.close()

    # data.update({"mars_fact_table":mars_table_html})


# # def images():
#     executable_path = {'executable_path': 'chromedriver.exe'}
#     browser = Browser('chrome', **executable_path, headless=False)

    #Cerebrus

    cerb_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'

    response = requests.get(cerb_url)
    soup = bs(response.text, 'lxml')

    cerb_title = soup.find('title').text
    cerb_title = cerb_title.split('|')
    cerb_title = cerb_title[0]

    cerb_hemisphere = soup.find_all('div', class_='wide-image-wrapper')
    cerb_hemisphere = cerb_hemisphere[0]
    cerb_hemisphere = cerb_hemisphere.find_all('img', class_='wide-image')
    cerb_hemisphere = cerb_hemisphere[0]
    cerb_hemisphere = cerb_hemisphere['src']

    
    hemis_base_url = 'https://astrogeology.usgs.gov/'
    cerb_full_url = hemis_base_url + cerb_hemisphere

    #Initialize dictionary to save url image and title
    hemis_image_urls = [
        {"title": cerb_title, "img_url": cerb_full_url}
    ]

    # Valles Marineris

    val_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    response = requests.get(val_url)
    soup = bs(response.text, 'lxml')

    val_title = soup.find('title').text
    val_title = val_title.split('|')
    val_title = val_title[0]

    val_hemisphere = soup.find_all('div', class_='wide-image-wrapper')
    val_hemisphere = val_hemisphere[0]
    val_hemisphere = val_hemisphere.find_all('img', class_='wide-image')
    val_hemisphere = val_hemisphere[0]
    val_hemisphere = val_hemisphere['src']

    val_full_url = hemis_base_url + val_hemisphere

    hemis_image_urls.append(
        {"title": val_title, "img_url": val_full_url})

    # Schiaparelli 

    sch_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'

    response = requests.get(sch_url)
    soup = bs(response.text, 'lxml')

    sch_title = soup.find('title').text
    sch_title = sch_title.split('|')
    sch_title = sch_title[0]

    sch_hemisphere = soup.find_all('div', class_='wide-image-wrapper')
    sch_hemisphere = sch_hemisphere[0]
    sch_hemisphere = sch_hemisphere.find_all('img', class_='wide-image')
    sch_hemisphere = sch_hemisphere[0]
    sch_hemisphere = sch_hemisphere['src']

    sch_full_url = hemis_base_url + sch_hemisphere

    hemis_image_urls.append(
        {"title": sch_title, "img_url": sch_full_url})

    #Syrtis Major

    syrtis_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'

    response = requests.get(syrtis_url)
    soup = bs(response.text, 'lxml')

    syrtis_title = soup.find('title').text
    syrtis_title = syrtis_title.split('|')
    syrtis_title = syrtis_title[0]

    syrtis_hemisphere = soup.find_all('div', class_='wide-image-wrapper')
    syrtis_hemisphere = syrtis_hemisphere[0]
    syrtis_hemisphere = syrtis_hemisphere.find_all('img', class_='wide-image')
    syrtis_hemisphere = syrtis_hemisphere[0]
    syrtis_hemisphere = syrtis_hemisphere['src']

    ##Construct full image URL
    syrtis_full_url = hemis_base_url + syrtis_hemisphere

    ##Add to dictionary
    hemis_image_urls.append(
        {"title": syrtis_title, "img_url": syrtis_full_url})

    browser.quit()

    # data.update({"hemis_images": hemis_image_urls})

    data = {"latest_news": header, 
            "Teaser": teaser,
            "featured_image": featured_image_url,
            "mars_fact_table": mars_table_html,
            "hemis_images": hemis_image_urls
    }
    return data
    

# def scrape():
#     headline()
#     featured_image()
#     facts()
#     images()
#     print(headline())
#     return data
