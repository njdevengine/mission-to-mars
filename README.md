## Mission to Mars: Flask, Mongo, Webscraping, Bootstrap...

```python
import requests
from bs4 import BeautifulSoup

#/from browser : inspect / network tab / Headers = headers / Form Data = login_data
with requests.Session() as s:
    url = 'https://mars.nasa.gov/news/'
    headers = {"user-agent" : "your browser info here"}
    r = s.get(url, headers=headers)
html = r.content.decode()
```


```python
soup = BeautifulSoup(html, 'html.parser')
nasa_news_header = soup.find('div', class_='content_title').find('a').text
nasa_news_teaser = soup.find('div', class_='rollover_description_inner').text
print(nasa_news_header)
print(nasa_news_teaser)
```

    
    NASA's Curiosity Mars Rover Finds a Clay Cache
    
    
    The rover recently drilled two samples, and both showed the highest levels of clay ever found during the mission.
    



```python
mars_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
with requests.Session() as s:
    r = s.get(mars_images_url)
html2 = r.content.decode()

soup = BeautifulSoup(html2, 'html.parser')

mars_images_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
mars_images_url = 'https://www.jpl.nasa.gov' + mars_images_url

print(mars_images_url)
```

    https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA17044-1920x1200.jpg


#### Weather in MARS


```python
mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
with requests.Session() as s:
    r = s.get(mars_weather_url)
html3 = r.content.decode()

soup = BeautifulSoup(html3)

tweets = soup.find_all('div', class_='js-tweet-text-container')

for tweet in tweets:
    mars_weather = tweet.find('p').text
    if 'Sol' and 'pressure' in weather:
        print(mars_weather)
        break
    else:
        pass
```

    InSight sol 190 (2019-06-09) low -104.1ºC (-155.3ºF) high -22.5ºC (-8.5ºF)
    winds from the SSE at 4.6 m/s (10.3 mph) gusting to 16.6 m/s (37.1 mph)
    pressure at 7.60 hPapic.twitter.com/Z6vS1S8RJo


#### Facts about  MARS


```python
import lxml
import pandas as pd

mars_facts_url = 'http://space-facts.com/mars/'
mars_facts = pd.read_html(mars_facts_url)
mars_facts_df = mars_facts[0]
mars_facts_df.columns = ['Description','Value']
mars_facts_df.set_index('Description', inplace=True)
mars_facts_df.to_html()

mars_facts_df2 = mars_facts_df.reset_index()
headers = list(mars_facts_df2["Description"])
values = list(mars_facts_df2["Value"])

headers2 =[]
for i in headers:
    x=(i[:-1])
    headers2.append(x)
    
mars_dictionary = {}
for i in range(len(headers)):
    mars_dictionary[headers2[i]] = values[i]

mars_facts_df2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Description</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Equatorial Diameter:</td>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Polar Diameter:</td>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mass:</td>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moons:</td>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Orbit Distance:</td>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Orbit Period:</td>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Surface Temperature:</td>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>First Record:</td>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Recorded By:</td>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>



#### Hemispheres of MARS


```python
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
```


```python
for i in range(0,4):
    print(hemisphere_image_urls[i]["title"])
    print(hemisphere_image_urls[i]["img_url"])
    print("\n")
```

    Cerberus Hemisphere Enhanced
    https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg
    
    
    Schiaparelli Hemisphere Enhanced
    https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg
    
    
    Syrtis Major Hemisphere Enhanced
    https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg
    
    
    Valles Marineris Hemisphere Enhanced
    https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg
    
    



```python
mars_data = {}
mars_data["data"] = mars_dictionary
mars_data["hemisphere_image_urls"] = hemisphere_image_urls
mars_data["mars_weather"] = mars_weather
mars_data["mars_images_url"] = mars_images_url
mars_data["nasa_news_header"] = nasa_news_header
mars_data["nasa_news_teaser"] = nasa_news_teaser
```
