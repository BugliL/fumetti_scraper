# import the necessary packages
from fumetti.items import FumettiItem
import datetime
import scrapy

BASE_DOMAIN = "http://www.mangareader.net"
BASE_URL = "http://www.mangareader.net/kakegurui"
NEXT_XPATH = "//span[@class=\"next\"]/a/@href"
PAGE_XPATH = "//*[@id=\"mangainfo\"]/div[1]/span/text()"
CHAPTER_XPATH = "//*[@id=\"mangainfo\"]/div[1]/h1//text()"
IMG_XPATH = "//*[@id=\"img\"]"
FIRST_CHAPTER_XPATH = "//tr/td[1]/a"

class CoverSpider(scrapy.Spider):
    name = "fumetti"
    start_urls = [
        BASE_URL,
    ]
    i = 0

    def parse(self, response):
        url = response.xpath(FIRST_CHAPTER_XPATH)
        yield scrapy.Request(BASE_DOMAIN + url.xpath("@href").extract_first(), self.parse_page)

    def parse_page(self, response):
        for img in response.xpath(IMG_XPATH).xpath("@src").extract():
            chapter = response.xpath(CHAPTER_XPATH).extract_first()
            page = response.xpath(PAGE_XPATH).extract_first()
            page = page.replace("&nbsp;", "").replace("-", "").replace("Page ", "").replace("\xa0", "")
            yield FumettiItem(chapter=chapter, page=page, img=img)

        l = response.xpath(NEXT_XPATH).extract_first()
        yield response.follow(l, self.parse_page)
