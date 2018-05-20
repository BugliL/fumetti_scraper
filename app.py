from scraper.scraper.spiders.mangareader import Mangareader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
# spider = Mangareader(manga='a-bias-girl')
# process.crawl(spider)
process.crawl(Mangareader, manga='a-bias-girl')
# process.crawl(Mangareader(manga='a-bias-girl'))
process.start()

# pdf o cbr
