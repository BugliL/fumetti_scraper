# from scraper.scraper.spiders.mangareader import Mangareader
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
#
# process = CrawlerProcess(get_project_settings())
# # spider = Mangareader(manga='a-bias-girl')
# # process.crawl(spider)
# process.crawl(Mangareader, manga='a-bias-girl')
# # process.crawl(Mangareader(manga='a-bias-girl'))
# process.start()
# pdf o cbr

from PyQt5 import QtWidgets, uic
from os import sys, getcwd, listdir, rename
from scraper.scrapergui import ScraperGui

from os.path import join, isdir
from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTreeView, QWidget, QVBoxLayout, QListView, QMessageBox
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from pathlib import Path

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ScraperGui()
    window.show()
    sys.exit(app.exec_())

