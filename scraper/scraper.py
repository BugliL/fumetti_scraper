# import sys
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from scraper.scraper.spiders.mangareader import Mangareader
# # from .scraper.spiders.mangareader import Mangareader
# # from scraper.spiders.mangareader import Mangareader
#
# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         process = CrawlerProcess(get_project_settings())
#         # process.crawl(Mangareader, manga=manga_name, callback=self.update)
#         process.crawl(Mangareader, manga=sys.argv[1])
#         process.start()
#     # else:
#     #     process = CrawlerProcess(get_project_settings())
#     #     # process.crawl(Mangareader, manga=manga_name, callback=self.update)
#     #     process.crawl(Mangareader, manga='a-bias-girl')
#     #     process.start()
