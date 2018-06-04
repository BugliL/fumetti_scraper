# import the necessary packages
from scraper.scraper.spiders.base import Base


class Mangareader(Base):
    name = "mangareader"
    START_BASE_DOMAIN = NEXT_BASE_DOMAIN = "https://www.mangareader.net"
    NEXT_XPATH = "//span[@class=\"next\"]/a/@href"
    IMG_XPATH = "//*[@id=\"img\"]"
    FIRST_CHAPTER_XPATH = "//tr/td[1]/a"
