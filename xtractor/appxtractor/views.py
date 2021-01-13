from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import BookForm
from .models import Book


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
    # titles = []
    # contents = []
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
            title = text[0][0]
            content = text[1:]
            content = [x[0] for x in content]
            images = []
            for image in parsed_html.body.find_all('img'):
                image_bytes = image['src']
                images.append(image_bytes)
            file_t = File(title,content, images)
            files.append(file_t)
            # contents.append(content)
            # titles.append(title)
        except KeyError:
            print("No titles found")
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




def book_list(request):
    books = Book.objects.all()


    return render(request, 'book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'
