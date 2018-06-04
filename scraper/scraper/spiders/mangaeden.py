# import the necessary packages
from scraper.scraper.spiders.base import Base


class Mangaeden(Base):
    name = "mangaeden"
    NEXT_BASE_DOMAIN = "https://www.mangaeden.com"
    NEXT_XPATH = "//a[@class=\"next\"]/@href"
    FIRST_CHAPTER_XPATH = '(//tr/td[1]/a)[last()]'
    IMG_XPATH = "//*[@id=\"mainImg\"]"


class MangaedenEN(Mangaeden):
    START_BASE_DOMAIN = "https://www.mangaeden.com/en/en-manga"


class MangaedenIT(Mangaeden):
    START_BASE_DOMAIN = "https://www.mangaeden.com/it/it-manga"


