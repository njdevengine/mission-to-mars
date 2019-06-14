import requests
from bs4 import BeautifulSoup
import lxml
import pandas as pd

def scrape():
    with requests.Session() as s:
        url = 'https://mars.nasa.gov/news/'
        headers = {"user-agent" : "your browser info here"}
        r = s.get(url, headers=headers)
    html = r.content.decode()
    soup = BeautifulSoup(html, 'html.parser')
    nasa_news_header = soup.find('div', class_='content_title').find('a').text
    nasa_news_teaser = soup.find('div', class_='rollover_description_inner').text
    mars_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    with requests.Session() as s:
        r = s.get(mars_images_url)
    html2 = r.content.decode()

    soup = BeautifulSoup(html2, 'html.parser')

    mars_images_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    mars_images_url = 'https://www.jpl.nasa.gov' + mars_images_url
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    with requests.Session() as s:
        r = s.get(mars_weather_url)
    html3 = r.content.decode()

    soup = BeautifulSoup(html3)

    tweets = soup.find_all('div', class_='js-tweet-text-container')

    for tweet in tweets:
        mars_weather = tweet.find('p').text
    
    mars_facts_url = 'http://space-facts.com/mars/'
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ['Description','Value']
    mars_facts_df.set_index('Description', inplace=True)
    mars_facts_df = mars_facts_df.to_html(classes="table table-striped")

    # mars_facts_df2 = mars_facts_df.reset_index()
    # headers = list(mars_facts_df2["Description"])
    # values = list(mars_facts_df2["Value"])

    # headers2 =[]
    # for i in headers:
    #     x=(i[:-1])
    #     headers2.append(x)
        
    # mars_dictionary = mars_facts_df2
    # for i in range(len(headers)):
    #     mars_dictionary[headers2[i]] = values[i]
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    with requests.Session() as s:
        r = s.get(hemispheres_url)
    html3 = r.content.decode()

    soup = BeautifulSoup(html3, 'html.parser')

    items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    for item in items: 
        title = item.find('h3').text
        
        img_url = item.find('a', class_='itemLink product-item')['href']
        img_html = s.get(hemispheres_main_url + img_url).content.decode()
        
        soup = BeautifulSoup( img_html, 'html.parser')
        
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    mars_data = {}
    mars_data["data"] = mars_facts_df
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    mars_data["mars_weather"] = mars_weather
    mars_data["mars_images_url"] = mars_images_url
    mars_data["nasa_news_header"] = nasa_news_header
    mars_data["nasa_news_teaser"] = nasa_news_teaser
    return mars_data