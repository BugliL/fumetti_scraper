from sys import argv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    print(argv)
    # process = CrawlerProcess(get_project_settings())
    # process.crawl(Mangareader, manga=manga_name, callback=self.update)
    # process.start()
