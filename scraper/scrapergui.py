from PyQt5.QtWidgets import QMainWindow, QMessageBox
from .gui.gui import Ui_mainWindow

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
# from .scraper.spiders.mangareader import Mangareader
from scraper.scraper.spiders.mangareader import Mangareader
from multiprocessing import Process, Queue
from twisted.internet import reactor


class ScraperGui(QMainWindow):
    manga_info = {'chapters': [], 'pages': 0}

    def __init__(self):
        super(ScraperGui, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.fetch_button.clicked.connect(self.launch_scraper)
        self.ui.download_button.clicked.connect(self.download_imgs)
        self.setFixedSize(self.size())
        self.show()
        # self.crawler_process = CrawlerProcess(get_project_settings())
        self.crawler_process = CrawlerRunner(get_project_settings())

    def run_spider(self, manga_name):
        try:
            myreturn = []
            runner = CrawlerRunner()
            deferred = runner.crawl(Mangareader, manga=manga_name, callback=self.update_manga_info, ret=myreturn)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            self.manga_ret = myreturn
        except Exception:
            self._show_allert('Runtime Error')

    def launch_scraper(self, signal):
        manga_name = self.ui.manga_name.text()
        if manga_name:
            p = Process(target=self.run_spider, args=(manga_name,)) # TODO continuare da qui
            p.start()
            p.join()
            # # self.crawler_process.crawl(Mangareader, manga=manga_name, callback=self.update_manga_info)
            # # self.crawler_process.start(stop_after_crawl=)
            # # self.crawler_process.start()
            # self.crawler_process.crawl(Mangareader, manga=manga_name, callback=self.update_manga_info)
            # self.crawler_process.join()
            print(self.manga_info)
            # print(self.manga_ret)
            self.ui.chapters.setText(str(len(self.manga_info['chapters'])))
            self.ui.pages.setText(str(self.manga_info['pages']))
            if self.manga_info['pages']:
                self.ui.download_button.setEnabled(True)
            else:
                self._show_allert("Manga Not Found")
        else:
            self._show_allert("Manga Url Missing")

    def download_imgs(self, signal):
        print('download_imgs')
        # TODO remove manga_info

    def update_manga_info(self, data):
        print('-'*20, data)
        if data['chapter'] not in self.manga_info['chapters']:
            self.manga_info['chapters'].append(data['chapter'])
        self.manga_info['pages'] += 1
        print(self.manga_info)

    def _show_allert(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Stato")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
