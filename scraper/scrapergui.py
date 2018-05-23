from PyQt5.QtWidgets import QMainWindow, QMessageBox
from .gui.gui import Ui_mainWindow

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
# from .scraper.spiders.mangareader import Mangareader
from scraper.scraper.spiders.mangareader import Mangareader
from multiprocessing import Process, Queue
from twisted.internet import reactor

from os.path import exists, join
from os import makedirs, remove
from json import loads


class ScraperGui(QMainWindow):
    manga_info = {'chapters': [], 'pages': 0}
    manga_name = None
    manga_url = None
    json_dir = 'fetched'
    json_path = None

    def __init__(self):
        super(ScraperGui, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.fetch_button.clicked.connect(self.launch_scraper)
        self.ui.download_button.clicked.connect(self.download_imgs)
        self.setFixedSize(self.size())
        self.show()
        # self.crawler_process = CrawlerProcess(get_project_settings())

    def _prepare_to_scraper(self):
        self.manga_name = self.manga_url.replace("-", " ").title()
        self.json_path = join(self.json_dir, f"{self.manga_name}.json")
        if not exists(self.json_dir):
            makedirs(self.json_dir)
        else:
            if exists(join(self.json_path)):
                remove(self.json_path)

    def _run_spider(self, manga_url, manga_name):
        try:
            runner = CrawlerRunner()
            # deff = runner.crawl(Mangareader, manga_url=self.manga_url, json_path=self.json_path)
            deff = runner.crawl(Mangareader, manga_url=self.manga_url, manga_name=manga_name, json_path=self.json_path)
            deff.addBoth(lambda _: reactor.stop())
            reactor.run()
        except Exception:
            self._show_allert('Runtime Error')

    def launch_scraper(self, signal):
        self.manga_url = self.ui.manga_name.text()
        if self.manga_url:
            self._prepare_to_scraper()
            # process = CrawlerProcess(get_project_settings())
            # process.crawl(Mangareader, manga_url=self.manga_url, manga_name=self.manga_name, json_path=self.json_path)
            # process.start()
            p = Process(target=self._run_spider, args=(self.manga_url, self.json_path,)) # TODO continuare da qui
            p.start()
            p.join()
            # if exists(f"fetched/{self.manga_name}.json"):
            if exists(self.json_path):
                self.update_manga_info()
                self.ui.download_button.setEnabled(True)
            else:
                self._show_allert("Manga Not Found")
        else:
            self._show_allert("Manga Url Missing")

    def download_imgs(self, signal):
        print('download_imgs')
        self.manga_name = None
        # TODO remove manga_info

    def update_manga_info(self):
        with open(join(self.json_dir, f"{self.manga_name}.json"), "r") as j:
            for line in j.readlines():
                data = loads(line)
                if data['chapter'] not in self.manga_info['chapters']:
                    self.manga_info['chapters'].append(data['chapter'])
                self.manga_info['pages'] += 1
        self.ui.chapters.setText(str(len(self.manga_info['chapters'])))
        self.ui.pages.setText(str(self.manga_info['pages']))
    #     print('-'*20, data)
    #     if data['chapter'] not in self.manga_info['chapters']:
    #         self.manga_info['chapters'].append(data['chapter'])
    #     self.manga_info['pages'] += 1
    #     print(self.manga_info)

    def _show_allert(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Stato")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
