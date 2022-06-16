from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from .models import Book
from mediaverse.settings import MEDIA_URL, BASE_DIR


# В request хранятся данные запроса пользователя - данные сессии, cookie и т.д.
def index(request):
    books = Book.objects.all()
    context = {
        'books': books,
        'title': 'MediaSpace',
        'media_url': MEDIA_URL
    }
    return render(request, 'mainapp/index.html', context)


def search(request):
    print(BASE_DIR)
    query = request.GET.get('search_line')
    searched_books = Book.objects.filter(
        Q(title__icontains=query) | Q(title__icontains=query.capitalize()) |
        Q(author__icontains=query) | Q(author__icontains=query.capitalize()) |
        Q(author__icontains=query.lower().replace('е', 'ё', 1)) |
        Q(author__icontains=query.lower().replace('е', 'ё', 1).capitalize())
    )
    context = {
        'books': searched_books,
        'title': 'MediaSpace',
        'media_url': MEDIA_URL,
        'query': query
    }
    return render(request, 'mainapp/index.html', context)
