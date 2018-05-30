# import the necessary packages
from scraper.scraper.items import MangaPage
from scraper.scraper.spiders.base import Base
# from ..items import MangaPage
# from .base import Base
import scrapy

# TODO aggiungere parametro it/en
class Mangaeden(Base):
    name = "mangaeden"
    NEXT_BASE_DOMAIN = "https://www.mangaeden.com/"
    NEXT_XPATH = "//span[@class=\"next\"]/a/@href"
    FIRST_CHAPTER_XPATH = '(//tr/td[1]/a)[last()]' # TODO

class MangaedenEN(Mangaeden):
    START_BASE_DOMAIN = "https://www.mangaeden.com/en/en-manga"
    # NEXT_XPATH = "//span[@class=\"next\"]/a/@href"
    IMG_XPATH = "//*[@id=\"img\"]"


class MangaedenIT(Mangaeden):
    # BASE_DOMAIN = "https://www.mangaeden.com/it/it-manga"
    START_BASE_DOMAIN = "https://www.mangaeden.com/it/it-manga"
    # NEXT_XPATH = "//span[@class=\"next\"]/a/@href"
    IMG_XPATH = "//*[@id=\"img\"]"


