# import the necessary packages
import scrapy
from os.path import exists, join
from os import makedirs, remove, listdir


class Base(scrapy.Spider):
    custom_settings = {'ITEM_PIPELINES': {'scraper.scraper.pipelines.ScraperPipeline': 100}}
    # custom_settings = {'ITEM_PIPELINES': {'scraper.pipelines.ScraperPipeline': 100}}
    BASE_DOMAIN = ''

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.manga_url = kwargs.get('manga_url')
        self.manga_name = kwargs.get('manga_name')
        self.json_path = kwargs.get('json_path')
        # self.callback = kwargs.get('callback')
        # self.ret = kwargs.get('ret')
        # if self.ret:
        #     self.ret = []

        # if not self.manga_url or not self.manga_name or not self.json_path:
        if not self.manga_url or not self.manga_name or not self.json_path:
            raise Exception('Manga Url or Name or JsonPath Not Given')

        self.start_urls = [f"{self.BASE_DOMAIN}/{self.manga_url}"]
        # self.manga_dir = join('fetched', self.manga_name)
        # self.manga_dir = self.json_path
        # self.manga_json = join(self.manga_dir, f"{self.manga_name}.json")
        # if not exists(self.manga_dir):
        #     makedirs(self.manga_dir)
        # else:
        #     if exists(self.manga_json):
        #         remove(self.manga_json)
        # self.manga_json = join(self.json_path, f"{self.manga_name}.json")
        # if not exists(self.json_path):
        #     makedirs(self.json_path)
        # else:
        #     if exists(self.manga_json):
        #         remove(self.manga_json)
            # for fj in filter(lambda f: f.endswith('.json'), listdir(self.manga_dir)):
            #     remove(join(self.manga_dir, fj))
        # TODO dare la possibilità di selezionare da quale capitolo partire

    def parse(self, response):
        pass

    # def notify_callback(self, data):
    #     if self.callback:
    #         self.callback(data)
    #
    # def add_return(self, data):
    #     if self.ret:
    #         self.ret.append(data)
