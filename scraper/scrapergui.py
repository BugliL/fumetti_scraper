from PyQt5.QtWidgets import QMainWindow, QMessageBox
from .gui.gui import Ui_mainWindow
from scrapy.crawler import CrawlerRunner
from scraper.scraper.spiders.mangareader import Mangareader
from multiprocessing import Process
from twisted.internet import reactor
from os.path import exists, join
from os import makedirs, remove
from json import loads
from urllib import request


class ScraperGui(QMainWindow):
    AGENTS = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    manga_site = None
    manga_url = None
    manga_name = None
    manga_info = {'chapters': [], 'pages': 0}
    json_path = None
    json_dir = 'fetched'
    download_dir = 'temp_downloads'
    save_dir = 'manga'

    def __init__(self):
        super(ScraperGui, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.fetch_button.clicked.connect(self.launch_scraper)
        self.ui.download_button.clicked.connect(self.download_imgs)
        self.setFixedSize(self.size())
        self.show()

    def launch_scraper(self, signal):
        self.manga_url = self.ui.manga_name.text()
        self.manga_site = self.ui.manga_site.currentText()
        if self.manga_url and self.manga_site:
            self._prepare_to_scraper()
            p = Process(target=self._run_spider, args=(self.manga_url, self.json_path,)) # TODO continuare da qui
            p.start()
            p.join()
            if exists(self.json_path):
                self.update_manga_info()
                self.ui.download_button.setEnabled(True)
            else:
                self._show_allert("Manga Not Found")
        else:
            self._show_allert("Manga Url Missing")

    def update_manga_info(self):
        with open(join(self.json_dir, f"{self.manga_name}.json"), "r") as j:
            for line in j.readlines():
                data = loads(line)
                if data['chapter'] not in self.manga_info['chapters']:
                    self.manga_info['chapters'].append(data['chapter'])
                self.manga_info['pages'] += 1
        self.ui.chapters.setText(str(len(self.manga_info['chapters'])))
        self.ui.pages.setText(str(self.manga_info['pages']))

    def download_imgs(self, signal):
        # TODO ogni volta che finisce un capitolo sceglie il prossimo passo da fare
        print('download_imgs')
        cur_chapter = None
        # for d in data:
        #     chapter = d['chapter']
        #     page = d['page']
        #     img = d['img']
        #
        #     chapter_path = os.path.join(BASEPATH, chapter)
        #     if not os.path.isdir(chapter_path):
        #         os.mkdir(chapter_path)
        #
        #     print("downloading {} - {} - {}".format(chapter, page, img))
        #     request.urlretrieve(img, "{}/{}.jpg".format(chapter_path, page))
        # self._reset_info()

    def _prepare_to_scraper(self):
        self.manga_name = self.manga_url.replace("-", " ").title()
        self.json_path = join(self.json_dir, f"{self.manga_name}.json")
        if not exists(self.json_dir):
            makedirs(self.json_dir)
        else:
            if exists(join(self.json_path)):
                remove(self.json_path)

    def _get_site(self):
        if self.manga_site=='www.mangareader.net':
            return Mangareader
        else:
            raise Exception(f'MangaSite Not Supported ({self.manga_site})')

    def _run_spider(self, manga_url, manga_name):
        try:
            runner = CrawlerRunner()
            deff = runner.crawl(self._get_site(), manga_url=self.manga_url, manga_name=manga_name, json_path=self.json_path)
            deff.addBoth(lambda _: reactor.stop())
            reactor.run()
        except Exception:
            self._show_allert('Runtime Error')

    def _prapare_downloader(self):
        if not exists(self.download_dir):
            makedirs(self.download_dir)
        if not exists(join(self.save_dir, self.manga_name)):
            makedirs(join(self.save_dir, self.manga_name))
        # Act as a browser
        opener = request.build_opener()
        opener.addheaders = [('User-Agent', self.AGENTS)]
        request.install_opener(opener)
        return request

    def _reset_info(self):
        self.manga_site = None
        self.manga_url = None
        self.manga_name = None
        self.manga_info = {'chapters': [], 'pages': 0}
        self.json_dir = 'fetched'
        self.json_path = None

    def _show_allert(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Allert")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
