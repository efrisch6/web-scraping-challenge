from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser 
import time



def scrape():
    executable_path = {'executable_path': 'C:/Users/niesa/Bootcamp/Homework/web-scraping-challenge/Missions_to_Mars/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)
    html = browser.html
    time.sleep(1)

    soup = BeautifulSoup(html, 'html.parser')

    divs = soup.body.find_all('div', class_="grid_list_container")

    news_title = []
    news_p = []

    for div in divs:
        for each in div.find_all('div',class_="content_title"):
            news_title.append(each.a.text)
        for teaser in div.find_all('div',class_="article_teaser_body"):
            news_p.append(teaser.text)
    
    print(news_title[0])
    print(news_p[0])
    
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(img_url)
    img_html = browser.html

    img_soup = BeautifulSoup(img_html,'html.parser')

    featured_image_url = 'https://www.jpl.nasa.gov' + img_soup.find('section',class_='main_feature').a['data-fancybox-href']

    tweet_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(tweet_url)
    tweet_html = browser.html

    tweet_soup = BeautifulSoup(tweet_html,'html.parser')

    mars_weather = tweet_soup.find('div',class_='stream').ol.li.p.text

    facts_url ='https://space-facts.com/mars/'

    # fact_table = pd.read_html(facts_url)[0].to_html(classes="table")
    fact_table = pd.read_html(facts_url)[0].rename(columns={0:'Description',1:"Values"}).set_index('Description').to_html(classes="table")

    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    archive_url = 'https://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(archive_url)
    usgs_html = browser.html

    usgs_soup = BeautifulSoup(usgs_html,'html.parser')

    results = usgs_soup.find('div', class_="results").find_all('div', class_='description')


    # links = []
    titles = []
    # for result in results:
    #     links.append(result.a['href'])
    #     titles.append(result.h3.text)

    urls = []

    # for link in links:
    #     # browser.visit(usgs_url[:29] + link)
    #     browser.visit(archive_url[:23] + link) 
    #     new_html = browser.html
    #     new_soup = BeautifulSoup(new_html, 'html.parser')
    #     # urls.append(usgs_url[:29]+new_soup.find('div',id='wide-image').find(class_='wide-image')['src'])
    #     urls.append(archive_url[:23]+new_soup.find('div',id='wide-image').find(class_='wide-image')['src'])

    for each in results:
        title = each.h3.text
        browser.click_link_by_partial_text(title)
        new_html = browser.html
        new_soup = BeautifulSoup(new_html, 'html.parser')
        urls.append(archive_url[:23]+new_soup.find('div',id='wide-image').find(class_='wide-image')['src'])
        titles.append(title)
        browser.back()
        time.sleep(1)

    hemisphere_image_urls = []
    
    for x in range(len(urls)):
        my_dict = {
            'title': titles[x],
            'img_url': urls[x]
        }
        hemisphere_image_urls.append(my_dict)

    final_dict = {
        'news_title' : news_title[0],
        'news_paragraph' : news_p[0],
        'feature_image' : featured_image_url,
        'weather' : mars_weather,
        'fact_table' : fact_table,
        'hemisphere_images' : hemisphere_image_urls
    }

    browser.quit()

    return final_dict