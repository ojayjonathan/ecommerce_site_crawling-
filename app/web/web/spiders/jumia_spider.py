import scrapy
from web.items import WebItem
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
web_item = WebItem()
class JumiaSpider(scrapy.Spider):
    name = "jumia"
    #allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://www.jumia.co.ke/smart-tvs-2282/",
        "https://www.jumia.co.ke/digital-tvs/",
        "https://www.jumia.co.ke/plasma-tvs/",
        "https://www.jumia.co.ke/bluetooth-speakers/",
        "https://www.jumia.co.ke/scanners",
        "https://www.jumia.co.ke/smart-watches/",
        "https://www.jumia.co.ke/smartphones/",
        "https://www.jumia.co.ke/tablets/",
        "https://www.jumia.co.ke/cooking-ingredients/",
        "https://www.jumia.co.ke/computer-accessories/",
        "https://www.jumia.co.ke/monitors/",
        "https://www.jumia.co.ke/printers/",
        "https://www.jumia.co.ke/data-storage/",
        "https://www.jumia.co.ke/servers/",
        "https://www.jumia.co.ke/home-audio-speakers/",
        "https://www.jumia.co.ke/womens-dresses/"

        ]

    def parse(self, response):
        self.logger.info('crawling url {}'.format(response.url))
        category = response.xpath("//div[@class='brcbs col16 -pvs']/a/text()")[-2].get()
        sub_category = response.xpath("//div[@class='brcbs col16 -pvs']/a/text()")[-1].get()
        for item in response.xpath("//div[@class='-paxs row _no-g _4cl-3cm-shs']/article"):
            web_item['price'] = item.css('.prc::text').get()
            web_item['prev_price']= item.css('.old::text').get(default=web_item['price'])
            web_item['reviews'] = item.css(".rev::text").get(default='0')
            web_item['per_discount'] = item.css('.tag._dsct._sm::text').get(default='0')
            web_item['item_link'] = 'https://www.jumia.co.ke{}'.format(item.css('a.core::attr(href)').get())
            web_item['image_src'] = item.css('img').attrib['data-src']
            web_item['rating'] =item.css('.stars._s::text').get(default='0')
            web_item['description']=item.css("h3.name::text").get()
            web_item['category']=category
            web_item['sub_category']=sub_category


            if web_item['price'] !=None:
                yield web_item
        try:
           next_page = response.xpath('//div[@class="pg-w -pvxl"]/a')[-2].attrib['href']
        except:
            next_page = ''   
        '''if next_page != '' or None:
            next_url = 'https://www.jumia.co.ke{}'.format(next_page)
            yield scrapy.Request(next_url, callback=self.parse)'''



