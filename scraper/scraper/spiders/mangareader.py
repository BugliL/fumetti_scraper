# import the necessary packages
from scraper.scraper.items import MangaPage
from scraper.scraper.spiders.base import Base
# from ..items import MangaPage
# from .base import Base
import scrapy


class Mangareader(Base):
    name = "mangareader"
    BASE_DOMAIN = "http://www.mangareader.net"
    NEXT_XPATH = "//span[@class=\"next\"]/a/@href"
    PAGE_XPATH = "//*[@id=\"mangainfo\"]/div[1]/span/text()"
    CHAPTER_XPATH = "//*[@id=\"mangainfo\"]/div[1]/h1//text()"
    IMG_XPATH = "//*[@id=\"img\"]"
    FIRST_CHAPTER_XPATH = "//tr/td[1]/a"

    def parse(self, response):
        url = response.xpath(self.FIRST_CHAPTER_XPATH)
        yield scrapy.Request(self.BASE_DOMAIN + url.xpath("@href").extract_first(), self.parse_page)

    def parse_page(self, response):
        for img in response.xpath(self.IMG_XPATH).xpath("@src").extract():
            chapter = response.xpath(self.CHAPTER_XPATH).extract_first()
            page = response.xpath(self.PAGE_XPATH).extract_first()
            page = page.replace("&nbsp;", "").replace("-", "").replace("Page ", "").replace("\xa0", "")
            # kwargs = {'manga':self.manga_name, 'chapter':chapter, 'page':page, 'img':img}
            # self.notify_callback(manga=self.manga_name, chapter=chapter, page=page, img=img)
            # self.notify_callback(kwargs)
            # self.add_return(kwargs)
            # yield MangaPage(**kwargs)
            # yield MangaPage(manga=self.manga_name, chapter=chapter, page=page, img=img)
            # yield MangaPage(json_path=self.json_path, manga=self.manga_name, chapter=chapter, page=page, img=img)
            yield MangaPage(json_path=self.json_path, manga=self.manga_name, chapter=chapter, page=page, img=img)

        l = response.xpath(self.NEXT_XPATH).extract_first()
        yield response.follow(l, self.parse_page)
