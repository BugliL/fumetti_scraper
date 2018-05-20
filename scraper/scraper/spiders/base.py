# import the necessary packages
import scrapy
from os.path import exists, join
from os import makedirs, remove, listdir


class Base(scrapy.Spider):
    custom_settings = {'ITEM_PIPELINES': {'scraper.scraper.pipelines.ScraperPipeline': 100}}
    BASE_DOMAIN = ''

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.manga = kwargs.get('manga')

        if not self.manga:
            raise Exception('Manga Not Given')

        self.start_urls = [f"{self.BASE_DOMAIN}/{self.manga}"]
        self.manga_name = self.manga.replace("-", " ").title()
        self.manga_dir = join('fetched', self.manga_name)

        if not exists(self.manga_dir):
            makedirs(self.manga_dir)
        else:
            for fj in filter(lambda f: f.endswith('.json'), listdir(self.manga_dir)):
                remove(join(self.manga_dir, fj))
        # TODO dare la possibilità di selezionare da quale capitolo partire

    def parse(self, response):
        pass
