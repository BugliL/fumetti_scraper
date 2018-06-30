from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, QThread, Qt
from scrapy.crawler import CrawlerRunner
from scraper.gui.gui import Ui_mainWindow
from scraper.scraper.spiders.mangaeden import MangaedenEN, MangaedenIT
from scraper.scraper.spiders.mangareader import Mangareader
from multiprocessing import Process, Queue
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
    manga_site = None
    manga_url = None
    site_scraper = None
    site_dir = None
    manga_name = None
    manga_info = {'chapters': {}, 'pages': 0}
    json_path = None
    json_dir = 'fetched'
    download_dir = 'temp_downloads'
    save_dir = 'manga'
    method = ''

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
        if self.manga_url.endswith('/'):
            self.manga_url = self.manga_url[:-1]
            self.ui.manga_name.setText(self.manga_url)
        self.manga_site = self.ui.manga_site.currentText()
        self.ui.chapter_bar.setValue(0)
        self.ui.total_bar.setValue(0)

        if self.manga_url and self.manga_site:
            self._prepare_to_scraper()

            if not exists(self.json_path):
                self.scraper_worker.set_manga_info(site_manager=self.site_scraper,
                                                   manga_url=self.manga_url,
                                                   manga_name=self.manga_name,
                                                   json_path=self.json_path)
                self.scraper_worker_thread.start()
            else:
                self._update_manga_info()
        else:
            self._show_allert("Manga Url Missing")

    def download_imgs(self, signal):
        """
            Downloads and saves the manga
        """
        self._prapare_downloader()
        self.image_worker.set_manga_info(manga_info=self.manga_info,
                                         method=self.method,
                                         download_dir=self.download_dir,
                                         save_dir=self.save_dir,
                                         remove_tmp_imgs=self.ui.remove_tmp_imgs.isChecked())
        self.image_worker_thread.start()

    def _prepare_to_scraper(self):
        self.manga_name = self.manga_url.replace("-", " ").title()
        self.site_scraper = self._get_site()
        self.json_dir = join(self.json_dir, self.site_dir)
        self.json_path = join(self.json_dir, f"{self.manga_name}.json")
        if not exists(self.json_dir):
            makedirs(self.json_dir)
        else:
            if exists(self.json_path) and self.ui.recreate_json.isChecked():
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

    def _close_scraper(self):
        self.scraper_worker_thread.quit()
        self.scraper_worker_thread.wait()
        self._update_manga_info()

    def _update_manga_info(self):
        if exists(self.json_path):
            with open(join(self.json_dir, f"{self.manga_name}.json"), "r") as j:
                for line in j.readlines():
                    data = loads(line)
                    if data['chapter'] not in self.manga_info['chapters'].keys():
                        self.manga_info['chapters'][data['chapter']] = {f"{int(data['page']):05d}": data['img']}
                    else:
                        self.manga_info['chapters'][data['chapter']][f"{int(data['page']):05d}"] = data['img']
                    self.manga_info['pages'] += 1
            self.ui.chapters.setText(str(len(self.manga_info['chapters'].keys())))
            self.ui.chapter_pages.setText(str(len(self.manga_info['chapters'][max(self.manga_info['chapters'].keys())])))
            self.ui.pages.setText(str(self.manga_info['pages']))
            self.ui.download_button.setEnabled(True)
        else:
            self._show_allert("Manga Not Found")

    def _prapare_downloader(self):
        self.download_dir = join(self.download_dir, self.site_dir, self.manga_name)
        self.save_dir = join(self.save_dir, self.site_dir, self.manga_name)
        if not exists(self.download_dir):
            makedirs(self.download_dir)
        if not exists(self.save_dir):
            makedirs(self.save_dir)
        self.method = self.ui.output_format.currentText()

    def _close_downloader(self):
        self.image_worker_thread.quit()
        self.image_worker_thread.wait()

    def _reset_info(self):
        self.ui.download_button.setEnabled(False)
        self.manga_site = None
        self.manga_url = None
        self.site_scraper = None
        self.site_dir = None
        self.manga_name = None
        self.manga_info = {'chapters': {}, 'pages': 0}
        self.json_path = None
        self.json_dir = 'fetched'
        self.download_dir = 'temp_downloads'
        self.save_dir = 'manga'
        self.method = ''

        self.scraper_worker_thread = QThread()
        self.scraper_worker = ScraperWorker()
        self.scraper_worker.moveToThread(self.scraper_worker_thread)
        self.scraper_worker.chapter.connect(self.ui.chapters.setText, Qt.QueuedConnection)
        self.scraper_worker.chapter_pages.connect(self.ui.chapter_pages.setText, Qt.QueuedConnection)
        self.scraper_worker.manga_pages.connect(self.ui.pages.setText, Qt.QueuedConnection)
        self.scraper_worker.end.connect(self._close_scraper)
        self.scraper_worker.error.connect(self._show_allert)
        self.scraper_worker_thread.started.connect(self.scraper_worker.start_scraper)

        self.image_worker_thread = QThread()
        self.image_worker = ImageWorker()
        self.image_worker.moveToThread(self.image_worker_thread)
        self.image_worker.chapter_progress.connect(self.ui.chapter_bar.setValue, Qt.QueuedConnection)
        self.image_worker.manga_progress.connect(self.ui.total_bar.setValue, Qt.QueuedConnection)
        self.image_worker.end.connect(self._close_downloader)
        self.image_worker_thread.started.connect(self.image_worker.create_chapters)

    def _show_allert(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Allert")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class ScraperWorker(QObject):
    """
        Scraper Asynchronous Process
    """
    chapter = pyqtSignal(str)
    chapter_pages = pyqtSignal(str)
    manga_pages = pyqtSignal(str)
    end = pyqtSignal()
    error = pyqtSignal(str)
    site_manager = None
    manga_url = ''
    manga_name = ''
    json_path = ''

    def set_manga_info(self, site_manager, manga_url, manga_name, json_path):
        self.site_manager = site_manager
        self.manga_url = manga_url
        self.manga_name = manga_name
        self.json_path = json_path

    def start_scraper(self):
        queue = Queue()

        p = Process(target=self._run_spider, args=(queue,))
        p.start()

        while True:
            page = queue.get(timeout=120)  # if a page take 2 minutes for retrieve then exit
            if page is None:
                break
            self.notify_progress(page)

        p.join()
        self.end.emit()

    def _run_spider(self, queue):
        try:
            runner = CrawlerRunner()
            runner.crawl(Mangareader,
                         manga_url=self.manga_url,
                         manga_name=self.manga_name,
                         json_path=self.json_path,
                         queue=queue)
            d = runner.join()
            d.addBoth(lambda _: reactor.stop())
            reactor.run()
        except Exception as e:
            self.error.emit(str(e))

    def notify_progress(self, info):
        self.chapter.emit(str(info['chapter']))
        self.chapter_pages.emit(str(info['chapter_page']))
        self.manga_pages.emit(str(info['pages']))


class ImageWorker(QObject):
    """
        Image Downloader Asynchronous Process
    """
    AGENTS = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'
    chapter_progress = pyqtSignal(int)
    manga_progress = pyqtSignal(int)
    end = pyqtSignal()
    manga_info = {}
    method = ''
    download_dir = ''
    save_dir = ''
    rm_tmp_imgs = False

    def set_manga_info(self, manga_info, method, download_dir, save_dir, remove_tmp_imgs):
        self.manga_info = manga_info
        self.method = method
        self.download_dir = download_dir
        self.save_dir = save_dir
        self.rm_tmp_imgs = remove_tmp_imgs

    def create_chapters(self):
        # Act as a browser
        opener = request.build_opener()
        opener.addheaders = [('User-Agent', self.AGENTS)]
        request.install_opener(opener)

        _tot_ch = len(self.manga_info['chapters'])
        _cur_ch = 0

        for chapter in sorted(self.manga_info['chapters'].keys()):
            chapter_imgs = []
            chapter_dir = join(self.download_dir, chapter)

            if not exists(chapter_dir):
                makedirs(chapter_dir)

            _tot_img = len(self.manga_info['chapters'][chapter])
            _cur_img = 0

            self.manga_progress.emit(int(100 * _cur_ch / _tot_ch))
            self.chapter_progress.emit(0)

            for page, img in sorted(self.manga_info['chapters'][chapter].items()):
                img_path = f"{join(chapter_dir, page)}.jpg"

                if not exists(img_path):
                    request.urlretrieve(img, img_path)
                _cur_img += 1

                chapter_imgs.append(img_path)
                self.chapter_progress.emit(int(100 * _cur_img / (_tot_img + 1)))

            self._create_manga_chapter(chapter, chapter_dir, chapter_imgs)
            self.chapter_progress.emit(100)
            _cur_ch += 1

        self.manga_progress.emit(100)
        self.end.emit()

    def _create_manga_chapter(self, chapter, chapter_dir, imgs):
        if self.method == 'pdf':
            with open(f"{join(self.save_dir, chapter)}.pdf", "wb") as f:
                f.write(img2pdf.convert(imgs))
        elif self.method == 'cbz':
            with zipfile.ZipFile(f"{join(self.save_dir, chapter)}.cbz", 'w') as cbz:
                for img in imgs:
                    cbz.write(img, join(chapter, basename(img)))
        elif self.method == 'jpg':
            move(chapter_dir, self.save_dir)
        else:
            raise Exception(f'Output Format Not Supported ({method})')
        if self.rm_tmp_imgs and self.method != 'jpg':
            for img in imgs:
                remove(img)
