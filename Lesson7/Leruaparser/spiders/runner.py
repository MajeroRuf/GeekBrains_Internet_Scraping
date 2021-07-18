from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Leruaparser.spiders.leroymerlinru import LeroymerlinruSpider
from Leruaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    # input = ('')
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinruSpider, search='кисточка')

    process.start()