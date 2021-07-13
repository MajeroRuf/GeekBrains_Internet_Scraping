import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SuperjobSpider(scrapy.Spider):
    name = 'Superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//div[@class='_1h3Zg _2rfUm _2hCDz _21a7u']/a/@href").extract()
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath("//h1/text()").extract_first()
        vacancy_link = response.url
        vacancy_salary = response.xpath("//span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']/text()").extract()
        item = JobparserItem(name=vacancy_name, salary=vacancy_salary, link=vacancy_link)
        yield item
