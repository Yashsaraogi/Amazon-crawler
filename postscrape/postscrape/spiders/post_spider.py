from turtle import title
import scrapy
import json
import time
import json
#import cfscrape
#from fake_useragent import UserAgent


from scrapy import signals
from pydispatch import dispatcher




w1 = input("Enter your item: ")
# w2 = input("enter the no of page : ")
class QuotesSpider(scrapy.Spider):
    name = "amazon"
    # *** Change this url for your prefered search from hemnet.se ***
    start_urls = [f'https://www.amazon.in/s?k={w1}']
    globalIndex = 0
    results = {}
    
    def parse(self, response):
           
            
            for ad in response.css("div.a-spacing-base "):
             
                title = ad.css("div.s-title-instructions-style > div.a-row > h5.s-line-clamp-1 > span.a-size-base-plus::text").get()
                
                prices = ad.css("div.s-price-instructions-style > div.a-row > a.s-underline-link-text > span.a-price > span.a-offscreen::text").get()
                if prices != None:
                    prices = prices.replace('\u20b9', '')

                original_price = ad.css("div.s-price-instructions-style > div.a-row > a.s-underline-link-text > span.a-text-price > span.a-offscreen::text").get()
                if original_price != None:
                    original_price = original_price.replace('\u20b9', '')

                description = ad.css("div.s-title-instructions-style > h2.a-size-mini > a.a-link-normal > span.a-size-base-plus::text").get()

                review = ad.css("div.a-spacing-top-micro > div.a-row  > span::attr(aria-label)").get()

                No_of_review = ad.css("div.a-spacing-top-micro > div.a-row  > span::attr(aria-label)")[1].get()

                id = ad.css("div.s-title-instructions-style > h2.a-size-mini > a.a-link-normal::attr(href)").get()
                start = id.find('dp/') +3
                end = id.find('/ref')
                id = id[start:end]

                prime_tag = ad.css("div.a-spacing-top-micro > div.a-row  > div.s-align-children-center > span.s-image-logo-view > span.s-prime > i::attr(aria-label)").get()
                Deal_of_day = ad.css("div.a-spacing-top-micro > div.a-row > a.a-link-normal > span::attr(id)").get()
                best_seller = ad.css("div.a-spacing-none > div.a-link-normal  >  span.rush-component > div.a-row > span::attr(id)").get()

                if len(id) == 10:
                    sponsered = "False"
                else :
                    sponsered = "True"
                
                yield {
                'Category' : w1 ,
                'Deal_of_day' : Deal_of_day,
                'best_seller' : best_seller,   
                'title': title,
                'description': description,
                'price': prices,
                'original-price' : original_price,
                'review' : review ,
                'No_of_review' : No_of_review,  
                'id' : id,
                'sponsered' : sponsered,
                'prime_tag' : prime_tag 
                }
            # next_page = response.css('div.a-section > span.s-pagination-strip >a.s-pagination-next::attr(href)').get() 
            # w2 = w2-1          
            # if w2 > 0 :
            #     if next_page is not None:
            #         next_page = response.urljoin(next_page)
            #         yield scrapy.Request(next_page, callback=self.parse)
               
                    
        
            
         
            

    