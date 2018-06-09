from os import sys
from PyQt5 import QtWidgets
from scraper.scrapergui import ScraperGui

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ScraperGui()
    window.show()
    sys.exit(app.exec_())

