import os
import django

from bs4 import BeautifulSoup
import requests

import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mediaverse.settings")
django.setup()

from mainapp.models import Book

# base_url = 'https://www.livelib.ru/genre/Классическая-литература/'
url = 'https://www.livelib.ru/genre/Классическая-литература/listview/biglist'

page = requests.get(url)
page.encoding = 'utf-8'

# soup = BeautifulSoup(page.text, "html.parser")

###
filtered_books = []

if page.status_code == 200:
    soup = BeautifulSoup(page.text, "html.parser")

    all_books_name = soup.findAll('a', class_='brow-book-name with-cycle')
    all_books_author = soup.findAll('a', class_='brow-book-author')
    all_books_isbn = soup.findAll('span', itemprop='isbn')

    all_books_links = soup.findAll('span', class_='brow-book-name with-cycle')

    all_books_year = soup.findAll('td', style='', itemprop='')
    filtered_books_year = []
    for year in all_books_year:
        if re.search(r'^\d\d\d\d$', year.text) is not None:
            filtered_books_year.append(year)

    all_books_links = soup.findAll('a', class_='brow-book-name with-cycle')
    book_links = []
    for item in all_books_links:
        book_links.append(re.findall(r'"[\w\/-]+"', str(item))[0].replace('"', ''))

    for book, author, isbn, year, book_link in zip(all_books_name,
                                                   all_books_author,
                                                   all_books_isbn,
                                                   filtered_books_year,
                                                   book_links):
        filtered_books.append([book.text, author.text, [isbn.text], year.text, book_link])

    all_books_image = soup.findAll('div', class_='cover-wrapper')
    urls = []
    for image_block in all_books_image:
        image_block = str(image_block.find(class_='cover-rounded'))
        a = re.findall(r'https:\/\/[\w.\/]+', image_block)
        urls.append(a[0])

    counter = 0
    for link in urls:
        cover_name = urls[counter].split("/")[-1]
        print(link)
        image = requests.get(link)
        out = open('../mediaverse/media/images/books/' + cover_name, 'wb')
        out.write(image.content)
        out.close()
        counter += 1

    for i in range(0, len(filtered_books)):
        filtered_books[i].append('images/books/' + urls[i].split("/")[-1])

all_books = Book.objects.all()

for item in filtered_books:
    new_book = Book(isbn=item[2][0],
                    title=item[0],
                    author=item[1],
                    year=item[3],
                    image=item[-1],
                    book_link=item[-2])

    is_existing = False
    for existing_book in all_books:
        example = str(new_book.title) + " (" + str(new_book.author) + ")"
        if existing_book.equals(example):
            if existing_book.book_link == '':
                book_to_update = Book.objects.get(book_id__exact=str(existing_book.book_id))
                book_to_update.book_link = new_book.book_link
                book_to_update.save()

                is_existing = True
                break
            else:
                print("Book " + new_book.title + " - " + new_book.author + " already exists!")
                is_existing = True
                break

    if not is_existing:
        new_book.save()
