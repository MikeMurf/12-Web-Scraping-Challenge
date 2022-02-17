### Mission_to_Mars
#### Step 2.1 Convert Jupyter Notebook to Python 

#   Set up Dependencies - Import Splinter, BeautifulSoup, and ChromeDriverManager 
from splinter import Browser
from bs4 import BeautifulSoup as soup
from datetime import datetime
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from flask_pymongo import PyMongo

#   Define the "scrape" function
def scrape():

    #   Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #   Set URL to the Mars Nasa News site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #   Include Delay for Loading the Page
    time.sleep(1)

    browser.is_element_present_by_css('div.list_text')

    #   Scrape the page into soup
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    slide_elem.find('div', class_='content_title')

    #   Use Parent Element to Find First Tag and Save it as "news title"
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_title

    #   Use Parent Element to Find Paragraph Text
    news_para = slide_elem.find('div', class_='article_teaser_body').get_text()
    news_para

    #   Set URL to the Mars Space Images site
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #   Find Full Image button and click
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #   Scrape the page into soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_soup

    #   Find the Relative Image
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_url_rel

    #   Use base URL to Create Absolute URL
    featured_img_url_1 = f'https://spaceimages-mars.com/{img_url_rel}'
    featured_img_url_1

    #   Set URL to the Mars Facts Site
    df_facts = pd.read_html('https://galaxyfacts-mars.com')[0]
    df_facts.head()

    #   Set "Description" as Index to DF
    df_facts.columns=['Description', 'Mars', 'Earth']
    df_facts.set_index('Description', inplace=True)
    df_facts

    #   Convert DF to HTML
    df_facts = df_facts.to_html(classes = "table table-striped")
        
    #   Set URL to Mars Hemispheres Site 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    #   Create List to hold Images
    hemis_image_urls = []

    #   Retrieve Image URLs and Titles for each Hemisphere.
    for hemis in range(4):
        #   Browse through each article
        browser.links.find_by_partial_text('Hemisphere')[hemis].click()
        
        #   Parse the HTML
        html = browser.html
        hemi_soup = soup(html,'html.parser')
        
        #   Scraping
        title = hemi_soup.find('h2', class_='title').text
        img_url = hemi_soup.find('li').a.get('href')
        
        #   Store Findings in a Dictionary and Append to List
        hemis = {}
        hemis['img_url'] = f'https://marshemispheres.com/{img_url}'
        #featured_img_url_1 = f'https://spaceimages-mars.com/{img_url}'

        hemis['title'] = title
        hemis_image_urls.append(hemis)
        
        #   Return
        browser.back()

    #   Display List that holds the Dictionary of each Image URL and Title.
    #print(news_title)
    #print(news_para)
    #print(img_url)
    #print(df_facts)
    #print(hemis_image_urls)

    #   Store Mars data in a dictionary
    mars_data = {
        'news_title': news_title,
        'news_para': news_para,
        'featured_image_url': featured_img_url_1,
        'mars_facts': df_facts,
        'hemisphere_image_urls' : hemis_image_urls
    }
     #   Close the browser after scraping
    browser.quit()

    print(mars_data)
   
    # datetime object containing current date and time
    now = datetime.now()
    #print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #print("date and time =", dt_string)	

    #   Return the Mars data results
    return mars_data

