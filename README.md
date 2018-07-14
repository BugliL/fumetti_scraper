# Manga Scraper Gui

## Supported Sites
- www.mangaeden.com
- www.mangareader.net

## Supported OutPut Formats
- PDF (one pdf for chapter)
- CBZ (one archive for chapter)
- JPG (one folder for chapter with images inside)

## Install dependencies through Anaconda 

```
$ conda create -n scraper python=3.6
$ conda install -n scraper scrapy PyQt
$ source activate scraper
(scraper) $ pip install img2pdf
```

## Start the Gui
**On Linux**
```
$ source activate scraper
(scraper) $ python app.py
(scraper) $ source deactivate
```

**On Windows**
```
activate scraper
python app.py
deactivate
```
or double click on `app.bat`


## Thanks
[BugliL](https://github.com/BugliL) from which i forked the project.