# Scrapy Fumetti
Versione per Python3

## Installazione prerequisiti

```
$ sudo apt-get install libffi-dev
$ sudo apt-get install libssl-dev
$ sudo apt-get install libxml2-dev libxslt1-dev
$ sudo apt-get install convert
```

## Installazione dipendenze

```
$ pip install pillow
$ pip install scrapy
```

## Lanciare l'applicazione
```
$ rm output.json
$ scrapy crawl fumetti -o output.json
$ python download.py
```

## Usando un unico comando
```
$ cd fumetti
$ rm output.json; scrapy crawl fumetti -o output.json; python download.py
$ ./convert_to_pdf
```

## Per non avere problemi cancellare i contenuti delle cartelle PDF e IMMAGINI

