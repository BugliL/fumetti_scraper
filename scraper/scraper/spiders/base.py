import scrapy
from scraper.scraper.items import MangaPage


class Base(scrapy.Spider):
    """
        Base Scraper Class, gives the generic behaviour
    """
    custom_settings = {'ITEM_PIPELINES': {'scraper.scraper.pipelines.ScraperPipeline': 100}}
    START_BASE_DOMAIN = ''
    NEXT_BASE_DOMAIN = ''
    FIRST_CHAPTER_XPATH = ''
    IMG_XPATH = ''
    NEXT_XPATH = ''
    parsed_pages = 0

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

        self.manga_url = kwargs.get('manga_url')
        self.manga_name = kwargs.get('manga_name')
        self.json_path = kwargs.get('json_path')
        self.queue = kwargs.get('queue')

        if not self.manga_url or not self.manga_name or not self.json_path:
            raise Exception('Manga Url or Name or JsonPath Not Given')

        self.start_url = f"{self.START_BASE_DOMAIN}/{self.manga_url}"
        self.start_urls = [self.start_url]

    def parse(self, response):
        url = response.xpath(self.FIRST_CHAPTER_XPATH)
        yield scrapy.Request(self.NEXT_BASE_DOMAIN + url.xpath("@href").extract_first(), self._parse)

    def _parse(self, response):
        for img in response.xpath(self.IMG_XPATH).xpath("@src").extract():
            cur_url = response.url[len(self.start_url)+1:]
            cur_url = cur_url[:-1] if cur_url.endswith('/') else cur_url
            if cur_url.count('/') == 0:
                chapter = cur_url
                page = '1'
            elif cur_url.count('/') == 1:
                chapter, page = cur_url.split('/')
            else:
                raise ValueError(f'Unexpected url: {response.url}. Send it to github.')

            if img.startswith('//'):
                img = f"http:{img}"

            self.parsed_pages += 1
            self.queue.put(dict(chapter=chapter, chapter_page=page, pages=self.parsed_pages))

            yield MangaPage(json_path=self.json_path,
                            manga=self.manga_name,
                            chapter=f"{self.manga_name} {int(chapter):05d}",
                            page=f"{int(page):05d}",
                            img=img)

        yield response.follow(response.xpath(self.NEXT_XPATH).extract_first(), self._parse)

    @staticmethod
    def close(spider, reason):
        spider.queue.put(None)
        super().close(spider, reason)

