"""
Start by converting your Jupyter notebook into a Python script called scrape_mars.py 
with a function called scrape that will execute all of your scraping code from above and 
return one Python dictionary containing all of the scraped data.
"""
from bs4 import BeautifulSoup as bs 
import os
import requests
from splinter import Browser
import time
import lxml.html as lh
import pandas as pd
# https://splinter.readthedocs.io/en/latest/drivers/chrome.html

def init_browser():
    executable_path = {'executable_path': '../chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

#web scraping preparation end
#==============================
def scrape():
    browser = init_browser()
    scrape_dic={}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup = bs(html,"html.parser")

    #NASA Mars News
    scrape_dic['Mars_news']=MarsNews()
    scrape_dic['featured_image_url']=MarsImage()
    scrape_dic['mars_weather']=MarsWeather()
    scrape_dic['mars_facts']=MarsFacts()
    scrape_dic['mars_hemisphere']=MarsHemisphere()
    return scrape_dic

def MarsNews():
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup = bs(html,"html.parser")
    #retrieve the title of the latest news 
    # using sleep() to hault the code execution 
    #wait until the url open in the browser 
    time.sleep(3)
    news_title=soup.find("div",class_="content_title").text
    #retrieve the paragraph text of the latest news 
    news_p = soup.find("div", class_="article_teaser_body").text
    #print(f'news_title = {news_title}')
    #print(f'news_p = {news_p}')
    #scrape_dic['news_title']=news_title
    #scrape_dic['news_content']=news_p
    marsnews= [news_title, news_p]
    return marsnews
    
#========================
#JPL Mars Space Images - Featured Image
#Visit the url for JPL Featured Space Image
def MarsImage():
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    html=browser.html
    soup = bs(html,"html.parser")
    time.sleep(3)
    featured_image_src = soup.find_all("a",class_="fancybox")[1]['data-fancybox-href']
    # URL for large size image 
    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_src
    #print(f'featured_image_url ={featured_image_url}')
    
    #scrape_dic['featured_image_url']=featured_image_url

    return featured_image_url
def MarsWeather():
    url3="https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    time.sleep(3)
    #find text massage by using xpath, there was no class name for the text 
    xpath = "/html/body/div/div/div/div/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div/div[1]/div/article/div/div[2]/div[2]/div[2]/span"
    mars_weather = browser.find_by_xpath(xpath).text
    #print(f'mars weather = {mars_weather}')
    #scrape_dic['mars_weather']=mars_weather
    return mars_weather

def MarsFacts():
    #Use Pandas to convert the data to a HTML table string
    url4 = "https://space-facts.com/mars/"
    browser.visit(url4)
    #read webpage in table form 
    table = pd.read_html(url4)
    #type(tables)
    #get the desired table 
    df = table[0]
    #rename the columns
    df.columns =["Facts","Values"]
    #transform table to html format
    html_table = df.to_html()
    html_table.replace('\n', '')
    #print(html_table)
    #scrape_dic['html_table']=[html_table]
    return html_table
def MarsHemisphere():
    url5="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    html=browser.html
    soup = bs(html,"html.parser")
    #find all the hemisphere titles in the webpage 
    title1=soup.find_all("img", class_="thumb")[0].attrs['alt']
    title2=soup.find_all("img", class_="thumb")[1].attrs['alt']
    title3=soup.find_all("img", class_="thumb")[2].attrs['alt']
    title4=soup.find_all("img", class_="thumb")[3].attrs['alt']
    #Cerberus Hemisphere (title1)
    title_link1 = soup.find("a",class_="itemLink").attrs['href']
    title_url1="https://astrogeology.usgs.gov" + title_link1
    #print(f'title: {title1}, img_url:{title_url1}')
    #Cerberus Hemisphere  high solution img 
    browser.visit(title_url1)
    #give time to reload the browser
    time.sleep(3)
    xpath1="/html/body/div[1]/div[1]/div[2]/div/ul/li[1]/a"
    img1=browser.find_by_xpath(xpath1).click()
    #after getting the first link successfully, use the same method to find the rest of all links 
    #find the rest of links
    all_links = soup.find_all("a",class_="itemLink")
    #Schiaparelli Hemisphere
    raw_link2 = all_links[3]
    title_link2 = raw_link2.attrs['href']
    title_url2 = "https://astrogeology.usgs.gov" + title_link2
    #print(f'title: {title2}, img_url:{title_url2}')
    
    #Schiaparelli Hemisphere img
    browser.visit(title_url2)
    time.sleep(3)
    xpath2="/html/body/div[1]/div[1]/div[2]/div/ul/li[1]/a"
    img2=browser.find_by_xpath(xpath2).click()
    #Syrtis Major Hemisphere
    raw_link3 = all_links[5]
    #Syrtis Major Hemisphere
    title_link3 = raw_link3.attrs['href']
    title_url3 = "https://astrogeology.usgs.gov" + title_link3
    #print(f'title: {title3}, img_url:{title_url3}')
    
    #Syrtis Major Hemisphere img
    browser.visit(title_url3)
    time.sleep(3)
    xpath3="/html/body/div[1]/div[1]/div[2]/div/ul/li[1]/a"
    img3=browser.find_by_xpath(xpath3).click()
    #Valles Marineris Hemisphere 
    raw_link4 = all_links[7]
    #Valles Marineris Hemisphere 
    title_link4 = raw_link4.attrs['href']
    title_url4 = "https://astrogeology.usgs.gov" + title_link4
    #print(f'title: {title4}, img_url:{title_url4}')
    
    #Valles Marineris Hemisphere img
    browser.visit(title_url4)
    time.sleep(3)
    xpath4="/html/body/div[1]/div[1]/div[2]/div/ul/li[1]/a"
    img4=browser.find_by_xpath(xpath4).click()
    #create four dictionaries contains hemisphere names and urls
    dic1={"title":title1,"img_url":title_url1}
    dic2={"title":title2,"img_url":title_url2}
    dic3={"title":title3,"img_url":title_url3}
    dic4={"title":title4,"img_url":title_url4}
    hemisphere_list=[dic1,dic2,dic3,dic4]
    #print(hemisphere_list)
    #scrape_dic['mars_hemisphere']=hemisphere_list
    #print(scrape_dic)
    return hemisphere_list


    
#==============


    
   

        



