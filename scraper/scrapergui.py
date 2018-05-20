from PyQt5.QtWidgets import QMainWindow, QMessageBox

from subprocess import call
from threading import Thread

from PyQt5.uic.properties import QtGui
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .scraper.spiders.mangareader import Mangareader
from .gui.gui import Ui_mainWindow


from PyQt5 import QtWidgets, uic
from os import sys, getcwd, listdir, rename
from os.path import join, isdir
from PyQt5.QtCore import QDir, Qt, QThread
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from pathlib import Path


# # class WorkerThread(QThread):
#     # def __init__(self, manga, callback=None):
#     def __init__(self):
#         super(WorkerThread, self).__init__()
#         # self.manga = manga
#         # self.callback = callback
#         # self.running = True
#
#     def run(self):
#         print('ciao')
#         # process = CrawlerProcess(get_project_settings())
#         # process.crawl(Mangareader, manga=self.manga, callback=self.callback)
#         # process.start()
#         # self.exit()
#         # self.running = False


class ScraperGui(QMainWindow):
    manga_info = {'chapters': [], 'chapter_pages': 0, 'pages': 0}

    def __init__(self):
        super(ScraperGui, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.fetch_button.clicked.connect(self.launch_scraper)
        self.ui.download_button.clicked.connect(self.download_imgs)


    def launch_scraper(self, signal):
        manga_name = self.ui.manga_name.toPlainText()
        if manga_name:
            # def scraper(manga, callback):
            #     process = CrawlerProcess(get_project_settings())
            #     process.crawl(Mangareader, manga=manga, callback=callback)
            #     process.start()
            # t = Thread(target=scraper, args=[manga_name, self.update])
            # t.start()
            # # w = WorkerThread(manga=manga_name, callback=self.update)
            # # w = WorkerThread()
            # # w.start()
            # # call(f"scraper.py ")
            process = CrawlerProcess(get_project_settings())
            process.crawl(Mangareader, manga=manga_name, callback=self.update_manga_info)
            process.start()
        else:
            self._show_allert("Manga Url Missing")

    def download_imgs(self, signal):
        print('download_imgs')
        # TODO remove manga_info

    def update_manga_info(self, data):
        print(data)
        if data['chapter'] not in self.manga_info['chapters']:
            self.manga_info['chapters'].append(data['chapter'])
            self.manga_info['chapter_pages'] = 1
            self.ui.chapters.setText(str(len(self.manga_info['chapters'])))
        else:
            self.manga_info['chapter_pages'] += 1
        self.manga_info['pages'] += 1
        self.ui.chapter_pages.setText(str(self.manga_info['chapter_pages']))
        self.ui.pages.setText(str(self.manga_info['pages']))
        # QtGui.qApp.processEvents()
        # QtGui.QMainWindow.update(self)
        # QMainWindow.update(self)
        self.ui.chapters.update()
        self.ui.chapter_pages.update()
        self.ui.pages.update()

    def _show_allert(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Stato")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
