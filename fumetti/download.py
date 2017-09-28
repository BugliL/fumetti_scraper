import os
from urllib import request
import json

OUTPUT = "output.json"
BASEPATH = "./immagini"

AGENTS = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'

data = open(OUTPUT).read()
data = json.loads(data)

# Act as a browser
opener = request.build_opener()
opener.addheaders = [('User-Agent', AGENTS)]
request.install_opener(opener)

for d in data:
    chapter = d['chapter']
    page = d['page']
    img = d['img']

    chapter_path = os.path.join(BASEPATH, chapter)
    if not os.path.isdir(chapter_path):
        os.mkdir(chapter_path)

    print("downloading {} - {} - {}".format(chapter, page, img))
    request.urlretrieve(img, "{}/{}.jpg".format(chapter_path, page))
