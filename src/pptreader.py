# from pptx import Presentation
import sys
import fitz
import re
from PIL import Image
import base64
import io

try:
    from BeautifulSoup import BeautifulSoup as bs
except ImportError: 
    from bs4 import BeautifulSoup as bs

filename = sys.argv[1]
doc = fitz.open(filename)
for page in doc:
    titles = []
    text = []
    images = []
    tables = []
    html = page.getText("html")
    parsed_html = bs(html,"lxml")
    # print(parsed_html)
    patt = re.compile("font-size:(\d+)")
    # element = parsed_html.body.find('span')
    # print(element['style'])
    for element in parsed_html.body.find_all('span'):
        content = element.text
        # print(element)
        element = element['style']
        # stripped = element.select("[style*=font-size]")
        # print(stripped)
        fontsize = int(patt.search(element).group(1))
        text_and_fontsize = (content,fontsize)
        text.append(text_and_fontsize)
    text.sort(key = lambda x : x[1], reverse=True)
    try:
        title = text[0][0]
        content = text[1:]
        # print(content[0])
        content = [x[0] for x in content]
        count = 1
        print("Title : ", format(title))
        print("Content :", format(content))
        print("\n")
        # for image in parsed_html.body.find_all('img'):
        #     image_bytes = image['src']
        #     filetype = image_bytes.split(',')[0]
        #     # if 'jpeg' in filetype or 'jpg' in filetype:
        #     image_bytes = image_bytes.split(',')[1]
        #     img = base64.b64decode(image_bytes)
        #     img = Image.open(io.BytesIO(img))
        #     img.save('images/' + title + '_' + str(count), "png")
        #     count+=1
    except KeyError:
        print("No titles on this page")
    