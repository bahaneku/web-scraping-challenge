from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests 
import scrape_mars

app=Flask(__name__)

app.config['MONGO_URI']='mongodb://localhost:27017/mars_app'
mongo=PyMongo(app)

@app.route('/')
def index():
    mars_data=mongo.db.mars_data.find_one()
    return render_template('index.html',mars_data=mars_data)

@app.route('/scrape')
def scrape():
    mars_data=mongo.db.mars_data
    mars_info=scrape_mars.scrape()
    mars_data.update({}, mars_info, upsert=True)
    return redirect('/')

if __name__=='__main__':
   app.run(debug=True)
