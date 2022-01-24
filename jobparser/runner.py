from scrapy.crawler import CrawlerProcess  # main process
from scrapy.settings import Settings

from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider
from jobparser import settings

if __name__ == '__main__':  # start of the app
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)  # read the settings

    process = CrawlerProcess(settings=crawler_settings)  # the process itself
    # process.crawl(SjruSpider)
    process.crawl(HhruSpider)

    process.start()
