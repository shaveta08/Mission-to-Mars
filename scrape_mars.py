from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def initBrowser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = initBrowser()
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(20)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('div', class_='list_text')
    description = title[0].find('div', class_='article_teaser_body')
    atag = title[0].find('a')
    print(atag.text)
    print(description.text)

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(10)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image = soup.find('img', class_="fancybox-image")
    featured_image_url = featured_image['src']
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
    print(featured_image_url)

    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    mars_facts = pd.DataFrame(tables[0])
    mars_facts.columns = ['Mars Fact', 'value']
    Facts = []
    for index, each in mars_facts.iterrows():
        index = index
        Facts.append({"fact": each['Mars Fact'], "value": each['value']})
    Facts
    #mars_facts.to_html("mars_facts1.html", header=True, index=False)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    all_links = soup.find_all('a', class_='itemLink product-item')

    hemi_links_header = []

    for each_link in all_links:
        title = each_link.find('h3')
        if title:
            a = each_link['href']
            a = "https://astrogeology.usgs.gov/" + a
            # visiting the first page and then getting the href
            browser.visit(a)
            time.sleep(10)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            div = soup.find('div', class_="downloads")
            a = div.find('a')
            url = a['href']
            hemi_links_header.append({"title": title.text, "img_url": url})

    result = {
        "title": atag.text,
        "description": description.text,
        "featured_link": featured_image_url,
        "mars_facts": Facts,
        "hemi_links_header1": hemi_links_header[0:2],
        "hemi_links_header2": hemi_links_header[2:4],
    }
    browser.quit()
    return result
