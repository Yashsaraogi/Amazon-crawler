from turtle import title
import scrapy
import json
import time
import json
#import cfscrape
#from fake_useragent import UserAgent
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlencode
from urllib.parse import urljoin
from scrapy import signals
from pydispatch import dispatcher
import pandas as pd

df = pd.read_csv('C:/Users/Asus/OneDrive/Desktop/crawler/postscrape/postscrape/spiders/Book1.csv')

item = df['Name'].tolist()
starturl =[]

for w1 in item:                                                     
   starturl.append(f'https://www.amazon.in/s?k={w1}')
print(starturl)

# w1 = input("Enter your item: ")
# starturl.append(f'https://www.amazon.in/s?k={w1}')   //  Comment line 20-22 and comment out line 24-25 to get input realtime rather than uploading csv file

API = '17a5880c2d8754577f3991c405ad5b5a'

def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)    #comment line 46-47 and comment out 29-32 and 44-45 if serval request has to made as it will avoid blockage of spider 
    return proxy_url

class QuotesSpider(scrapy.Spider):
    name = "amazon"
    # *** Change this url for your prefered search from hemnet.se ***
    start_urls = starturl
    print(start_urls)
    globalIndex = 0
    results = {}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=get_url(url), dont_filter=True, meta={'start_url': url},callback=self.parse,
            method="GET")
            # yield scrapy.Request(url, dont_filter=True, meta={'start_url': url},callback=self.parse,
            # method="GET")
    
    def parse(self, response):
           
            
            for ad in response.css("div.a-spacing-base "):
             
                title = ad.css("div.s-title-instructions-style > div.a-row > h5.s-line-clamp-1 > span.a-size-base-plus::text").get()

                
                prices = ad.css("div.s-price-instructions-style > div.a-row > a.s-underline-link-text > span.a-price > span.a-offscreen::text").get()
                if prices != None:
                    prices = prices.replace('\u20b9', '')

                original_price = ad.css("div.s-price-instructions-style > div.a-row > a.s-underline-link-text > span.a-text-price > span.a-offscreen::text").get()
                if original_price != None:
                    original_price = original_price.replace('\u20b9', '')

                description = ad.css("div.s-padding-right-small > div.s-title-instructions-style > h2.a-size-mini > a.a-link-normal > span.a-size-base-plus::text").get()
                

                review = ad.css("div.a-spacing-top-micro > div.a-row  > span::attr(aria-label)").get()

                No_of_review = ad.css("div.a-spacing-top-micro > div.a-row  > span > a.a-link-normal > span.a-size-base::text").get()

                id = ad.css("div.s-title-instructions-style > h2.a-size-mini > a.a-link-normal::attr(href)").get()

                
                start = id.find('dp/') +3
                end = id.find('/ref')
                id = id[start:end]
                

                if len(id) == 10:
                    sponsered = 0
                else :
                    sponsered = 1

                if len(id) == 10:
                    id = id
                else :
                    starts = id.find('dp%2') + 4
                    ends = id.find('%2Fref') 
                    id = id[starts:ends]

                prime_tag = ad.css("div.a-spacing-top-micro > div.a-row  > div.s-align-children-center > span.s-image-logo-view > span.s-prime > i::attr(aria-label)").get()

                Deal_of_day = ad.css("div.a-spacing-top-small > div.a-row > a.a-link-normal > span.a-badge > span.a-badge-label > span.a-badge-label-inner > span.a-badge-text::text").get()
                
                # best_seller = ad.css("div.s-image-overlay-grey > div.a-link-normal  >  span.rush-component > div.a-badge-region > span.a-badge > span.a-badge-label > span.a-badge-label-inner > span.a-badge-text::text").get()


                Amazon_choice = ad.css("div.s-image-overlay-grey > span::attr(aria-label)").get()
                
                
                start_url = response.meta['start_url']
                start1 = start_url.find('s?k=') + 4
                category = start_url[start1:]
                
                yield {
                'category' : category,
                'description': description,
                'title': title,
                'price': prices,
                'original-price' : original_price,
                'review' : review ,
                'No_of_review' : No_of_review,  
                'id' : id,
                'sponsered' : sponsered,
                'prime_tag' : prime_tag,
                
                'Deal_of_day' : Deal_of_day,
                'Amazon_choice' : Amazon_choice,
                # 'best_seller' : best_seller, 
                'start_url': response.meta['start_url'] ,
                }
            # next_page = response.css('div.a-section > span.s-pagination-strip >a.s-pagination-next::attr(href)').get() 
            # w2 = w2-1          
            # if w2 > 0 :
            #     if next_page is not None:
            #         next_page = response.urljoin(next_page)
            #         yield scrapy.Request(next_page, callback=self.parse)
               
                    
        
            
         
            

    