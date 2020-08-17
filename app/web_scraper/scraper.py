import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_url =['https://blog.scrapinghum.com']

    def parse(self, response):
        for title in response.css('.post-header>h2'):
            yield{'title':title.css('a::text').get()}
            print(title)
        for next_page in response.css('a.next-post-link'):
            yield response.follow(next_page, self.parse)

spider = BlogSpider()
