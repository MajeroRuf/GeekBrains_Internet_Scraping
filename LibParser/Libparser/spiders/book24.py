import scrapy
from scrapy.http import HtmlResponse
from Libparser.items import LibparserItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=python']
    next_page = f'https://book24.ru/search//page-1/?q=python'
    page =1

    def parse(self, response: HtmlResponse):
        book24_links = response.xpath("//a[@class='product-card__name smartLink']/@href").extract()
        page_exit = response.xpath("//div[@class='search-page__no-results']")
        print()
        for link in book24_links:
            yield response.follow(link, callback=self.vacansy_parse)
        self.page +=1
        self.next_page = f'https://book24.ru/search/page-{str(self.page)}/?q=python'
        if not page_exit:
            yield response.follow(self.next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        book_name = response.xpath("//h1[@class='product-detail-page__title']/text()").extract_first()
        book_link = response.url
        price_old = response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").extract()
        price_new = response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").extract()
        author = response.xpath("//div[@class='product-characteristic__item']"
                                "/div[@class='product-characteristic__value']"
                                "/a[@class='product-characteristic-link smartLink']/text()").extract_first()
        rate = response.xpath("//span[@class='rating-widget__main-text']/text()").extract()

        item = LibparserItem(name=book_name, price_old=price_old, price_new=price_new,
                             link=book_link, author=author, rate=rate)
        yield item

