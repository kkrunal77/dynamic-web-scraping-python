import os
import time
import requests
import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver


class static_javascript_web_scraping_pythonSpider(scrapy.Spider):
    name = "static_javascript_web_scraping_python"

    def start_requests(self):
        urls = list()
        # print("**"*80)
        chromedriver = "/home/kk/chromedriver_storage/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
        driver.get("https://www.sosnc.gov/online_services/search/by_title/_Business_Registration")
        element = driver.find_element_by_id("SearchCriteria")
        element.send_keys("a")
        element.submit()
        time.sleep(5)
        # print("**"*80)
        for i in range(2,4):
            print("start :",i)
            soup = BeautifulSoup(driver.page_source, "lxml")
            var = soup.find_all('a',{"class":"java_link"})
            for i in var:
                i = "https://www.sosnc.gov"+str(i['data-action'])
                print(i)
                yield scrapy.Request(url=i, callback=self.parse)
                urls.append(i)
            time.sleep(5)
            element = driver.find_element_by_id('NextPage') # Find the search box
            time.sleep(5)
            element.click()
            time.sleep(5)

            next_page = soup.find('li',{"class":"disabled"})
            print(next_page)
            if next_page:
                break
            print("End :",i)
            print('*'*40)
        # for url in urls:
            # yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        main_page = BeautifulSoup(response.body, "lxml")
        # print(main_page)

        dict_name = {"From_Url"  : response.url ,
        				"Html" : main_page}
        yield dict_name
        # next_page = main_page.find('a', text = 'Next 100 →')
        # print('**'*100)
        # print(next_page['href'])
        # if next_page:
        #     next_href = next_page['href']
        #     next_page_url = 'https://coinmarketcap.com/' + next_href
        #     print(next_page_url)
        #     request = scrapy.Request(url=next_page_url)
        #     yield request