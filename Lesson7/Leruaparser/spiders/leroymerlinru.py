import scrapy
from scrapy.http import HtmlResponse
from Leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LeroymerlinruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//a[contains(@class,'bex6mjh_plp b1f5t594_plp p5y548z_plp pblwt5z_plp nf842wf_plp')]")
        next_page = response.xpath("//a[contains(@data-qa-pagination-item,'right')]/@href").extract_first()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_good)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        print()
        yield loader.load_item()


