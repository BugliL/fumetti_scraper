from PyQt5.QtWidgets import QMainWindow, QMessageBox
from scrapy.crawler import CrawlerRunner
from scraper.gui.gui import Ui_mainWindow
from scraper.scraper.spiders.mangaeden import MangaedenEN, MangaedenIT
from scraper.scraper.spiders.mangareader import Mangareader
from multiprocessing import Process
from twisted.internet import reactor
from os.path import exists, join, basename
from os import makedirs, remove
from shutil import move
from json import loads
from urllib import request
import img2pdf
import zipfile


class ScraperGui(QMainWindow):
    """
        PyQt5 Gui, helps to fetch the manga url and to download it
    """
    AGENTS = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    manga_site = None
    manga_url = None
    site_dir = None
    manga_name = None
    manga_info = {'chapters': {}, 'pages': 0}
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
        """
            Starts the manga's fetch
        """
        self._reset_info()
        self.manga_url = self.ui.manga_name.text()
        self.manga_site = self.ui.manga_site.currentText()
        self.ui.chapter_bar.setValue(0)
        self.ui.total_bar.setValue(0)
        if self.manga_url and self.manga_site:
            self._prepare_to_scraper()
            p = Process(target=self._run_spider, args=(self._get_site(),))
            p.start()
            p.join()
            if exists(self.json_path):
                self._update_manga_info()
                self.ui.download_button.setEnabled(True)
            else:
                self._show_allert("Manga Not Found")
        else:
            self._show_allert("Manga Url Missing")

    def download_imgs(self, signal):
        """
            Downloads and saves the manga
        """
        self._prapare_downloader()
        _tot_ch = len(self.manga_info['chapters'])
        _cur_ch = 0
        for chapter in sorted(self.manga_info['chapters'].keys()):
            chapter_imgs = []
            chapter_dir = join(self.download_dir, chapter)
            if not exists(chapter_dir):
                makedirs(chapter_dir)
            _tot_img = len(self.manga_info['chapters'][chapter])
            _cur_img = 0
            self.ui.total_bar.setValue(int(100 * _cur_ch / _tot_ch))
            self.ui.chapter_bar.setValue(int(100 * _cur_img / _tot_img))
            self.ui.total_bar.update()
            self.ui.chapter_bar.update()
            for page, img in sorted(self.manga_info['chapters'][chapter].items()):
                img_path = f"{join(chapter_dir, page)}.jpg"
                if not exists(img_path):
                    request.urlretrieve(img, img_path)
                chapter_imgs.append(img_path)
                self.ui.chapter_bar.setValue(int(100 * _cur_img / _tot_img))
                self.ui.chapter_bar.update()
            self._create_manga_chapter(chapter, chapter_dir, chapter_imgs)
            self.ui.chapter_bar.setValue(100)
            self.ui.total_bar.update()
        self.ui.total_bar.setValue(100)
        self.ui.total_bar.update()

    def _prepare_to_scraper(self):
        self.manga_name = self.manga_url.replace("-", " ").title()
        self.json_path = join(self.json_dir, f"{self.manga_name}.json")
        if not exists(self.json_dir):
            makedirs(self.json_dir)
        else:
            if exists(join(self.json_path)):
                remove(self.json_path)

    def _get_site(self):
        if self.manga_site == 'www.mangaeden.com/en/en-manga':
            self.site_dir = join('Mangaeden', 'en')
            return MangaedenEN
        elif self.manga_site == 'www.mangaeden.com/it/it-manga':
            self.site_dir = join('Mangaeden', 'it')
            return MangaedenIT
        elif self.manga_site == 'www.mangareader.net':
            self.site_dir = 'Mangareader'
            return Mangareader
        else:
            raise Exception(f'MangaSite Not Supported ({self.manga_site})')

    def _run_spider(self, site_manager):
        try:
            runner = CrawlerRunner()
            deff = runner.crawl(site_manager, manga_url=self.manga_url, manga_name=self.manga_name,
                                json_path=self.json_path)
            deff.addBoth(lambda _: reactor.stop())
            reactor.run()
        except Exception:
            self._show_allert('Runtime Error')

    def _update_manga_info(self):
        with open(join(self.json_dir, f"{self.manga_name}.json"), "r") as j:
            for line in j.readlines():
                data = loads(line)
                if data['chapter'] not in self.manga_info['chapters'].keys():
                    self.manga_info['chapters'][data['chapter']] = {f"{int(data['page']):05d}": data['img']}
                else:
                    self.manga_info['chapters'][data['chapter']][f"{int(data['page']):05d}"] = data['img']
                self.manga_info['pages'] += 1
        self.ui.chapters.setText(str(len(self.manga_info['chapters'].keys())))
        self.ui.pages.setText(str(self.manga_info['pages']))

    def _prapare_downloader(self):
        self.download_dir = join(self.download_dir, self.site_dir, self.manga_name)
        self.save_dir = join(self.save_dir, self.site_dir, self.manga_name)
        if not exists(self.download_dir):
            makedirs(self.download_dir)
        if not exists(self.save_dir):
            makedirs(self.save_dir)
        # Act as a browser
        opener = request.build_opener()
        opener.addheaders = [('User-Agent', self.AGENTS)]
        request.install_opener(opener)

    def _create_manga_chapter(self, chapter, chapter_dir, imgs):
        method = self.ui.output_format.currentText()
        if method == 'pdf':
            with open(f"{join(self.save_dir, chapter)}.pdf", "wb") as f:
                f.write(img2pdf.convert(imgs))
        elif method == 'cbr':
            with zipfile.ZipFile(f"{join(self.save_dir, chapter)}.cbr", 'w') as cbr:
                for img in imgs:
                    cbr.write(img, join(chapter, basename(img)))
        elif method == 'jpg':  # FIXME rewrite
            move(chapter_dir, self.save_dir)
        else:
            raise Exception(f'Output Format Not Supported ({method})')

    def _reset_info(self):
        self.ui.download_button.setEnabled(False)
        self.manga_site = None
        self.manga_url = None
        self.site_dir = None
        self.manga_name = None
        self.manga_info = {'chapters': {}, 'pages': 0}
        self.json_path = None
        self.json_dir = 'fetched'
        self.download_dir = 'temp_downloads'
        self.save_dir = 'manga'

    def _show_allert(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Allert")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
