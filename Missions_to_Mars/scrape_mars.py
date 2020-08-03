# Importing dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pymongo
import requests
from splinter import Browser


def init_browser():
    executable_path = {'executable_path': '/Users/ekaster/Documents/DATABOOTCAMP-MATERIAL/chromedriver.exe'}
    return browser('chrome', **executable_path, headless=False)
    time.sleep(1)

def scrape_mars_data():
    browser = init_browser()
 
 # NASA MARS NEWS
    mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news_url)
    time.sleep(1)
    
    html = browser.html
    news_soup = bs(html, 'html.parser')
    
    news_title = news_soup.find("div", class_="content_title").text
    news_p = news_soup.find("div", class_="rollover_description_inner").text
 
# FEATURED IMAGE

    mars_img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_img_url)
    time.sleep(1)

    html_image = browser.html
    browser_soup = bs(html_image, 'html.parser')
    get_img_url = browser_soup.find('img', class_='main_image')
    img_src_url = get_img_url.get('src')
    featured_image_url = "https://www.jpl.nasa.gov" + img_src_url    

# MARS WEATHER

    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_twitter_url)
    time.sleep(1)

    html_weather = browser.html
    twitter_soup = bs(html_weather, 'html.parser')
    latest_tweets = twitter_soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').text

# MARS FACTS

    request_mars_space_facts = requests.get("https://space-facts.com/mars/")
    mars_space_table_read = pd.read_html(request_mars_space_facts.text)
    mars_space_table_read
    mars_df = mars_space_table_read[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index(['Description'], inplace=True)

    mars_data_html = mars_df.to_html()

# MARS HEMISPHERES

    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)
    time.sleep(1)

    mars_hemi_html = browser.html
    mars_hemi_soup = bs(mars_hemi_html, 'html.parser')
    items = mars_hemi_soup.find_all('div', class_='item')
    mars_hemi_img_url = []
    mars_hemi_main_url = 'https://astrogeology.usgs.gov'

    for i in items: 
        title = i.find('h3').text
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(mars_hemi_main_url + partial_img_url)
        partial_img_html = browser.html
        soup = bs( partial_img_html, 'html.parser')
        img_url = mars_hemi_main_url + soup.find('img', class_='wide-image')['src']
        mars_hemi_img_url.append({"title" : title, "img_url" : img_url})
    

# DICTIONARY
    mars_data = {'news_title': news_title,
                    'news_p': news_p,
                    'featured_image_url':featured_image_url,
                    'latest_tweets': latest_tweets,
                    'mars_data_html': mars_data_html,
                    'mars_hemi_img_url': mars_hemi_img_url
        }

    
    browser.quit()

        
    return mars_data