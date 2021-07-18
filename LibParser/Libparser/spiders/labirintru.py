import scrapy
from scrapy.http import HtmlResponse
from Libparser.items import LibparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/?stype=0']

    def parse(self, response: HtmlResponse):
        labirint_links = response.xpath("//a[@class='product-title-link']/@href").extract()
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").extract_first()
        for link in labirint_links:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        book_name = response.xpath("//h1/text()").extract_first()
        book_link = response.url
        price_old = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract()
        price_new = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract()
        author = response.xpath("//div[@class='authors']/a[@data-event-label='author']/text()").extract()
        rate = response.xpath("//div[@id='rate']/text()").extract()

        item = LibparserItem(name=book_name, price_old=price_old, price_new=price_new,
                             link=book_link, author=author, rate=rate)
        yield item