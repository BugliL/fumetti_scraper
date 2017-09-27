# import the necessary packages
from fumetti.items import FumettiItem
import datetime
import scrapy


class CoverSpider(scrapy.Spider):
    name = "fumetti"
    start_urls = [
        "http://www.mangareader.net/yu-gi-oh-gx",
    ]
    i = 0

    def parse(self, response):
        url = response.xpath("//tr/td[1]/a")
        yield scrapy.Request("http://www.mangareader.net" + url.xpath("@href").extract_first(), self.parse_page)

    def parse_page(self, response):
        for img in response.xpath("//*[@id=\"img\"]").xpath("@src").extract():
            chapter = response.xpath("//*[@id=\"mangainfo\"]/div[1]/h1//text()").extract_first()
            page = response.xpath("//*[@id=\"mangainfo\"]/div[1]/span/text()").extract_first()
            page = page.replace("&nbsp;", "").replace("-", "").replace("Page ", "")  # Page 1 -
            yield FumettiItem(chapter=chapter, page=page, img=img)

        l = response.xpath("//span[@class=\"next\"]/a/@href").extract_first()
        yield response.follow(l, self.parse_page)
