from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import SectionForm
from .models import Section


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


class Home(TemplateView):
    template_name = 'home.html'

class File:
    def __init__(self, title, content, images):
        self.title = title
        self.content = content
        self.images = images

def get_titles(filepath):
    
    files = []
    doc = fitz.open(filepath)
    for page in doc:
        text = []
        html = page.getText("html")
        parsed_html = bs(html,"lxml")
        patt = re.compile("font-size:(\d+)")
        for element in parsed_html.body.find_all('span'):
            content = element.text
            element = element['style']
            fontsize = int(patt.search(element).group(1))
            text_and_fontsize = (content,fontsize)
            text.append(text_and_fontsize)
        text.sort(key = lambda x : x[1], reverse=True)

        try:
            # print(text)
            title = text[0][0]
            content = []
            if len(text)>1:
                content = text[1:]
                content = [x[0] for x in content]
            images = []
            for image in parsed_html.body.find_all('img'):
                image_bytes = image['src']
                images.append(image_bytes)
            file_t = File(title,content, images)
            files.append(file_t)

        except IndexError:
            print("No titles found")
            continue

    return files


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        print(context)
        stringv = context['url']
        stringv = stringv[1:]
        print(stringv)
        files = get_titles(stringv)
        context['files'] = files
    return render(request, 'upload.html', context)