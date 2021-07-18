import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhRuSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath("//h1/text()").extract_first()
        vacancy_link = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract_first()
        vacancy_salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        item = JobparserItem(name=vacancy_name, salary=vacancy_salary, link=vacancy_link)
        yield item
