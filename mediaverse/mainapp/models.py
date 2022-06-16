from django.db import models


class BookGenre(models.Model):
    name = models.CharField(max_length=64, verbose_name="Наименование")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'жанр книги'
        verbose_name_plural = 'жанры книг'
        ordering = ['name']


class Book(models.Model):
    book_id = models.IntegerField(unique=True, primary_key=True, verbose_name="ID")
    isbn = models.CharField(max_length=64, null=True, blank=True, verbose_name="ISBN")
    title = models.CharField(max_length=512, verbose_name="Название")
    author = models.CharField(max_length=100, null=True, blank=True, verbose_name="Автор")
    year = models.IntegerField(null=True, blank=True, verbose_name="Год публикации")
    description = models.TextField(max_length=512, null=True, blank=True, verbose_name="Описание")
    genres = models.ManyToManyField(BookGenre, related_name='books', db_table='book_genre', verbose_name="Жанры")
    image = models.ImageField(max_length=1000, upload_to='images/books/', null=True, blank=True, verbose_name="Обложка")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    age_restrictions = models.CharField(max_length=50, default='18+', verbose_name="Возрастные ограничения")
    book_link = models.CharField(max_length=200, default='', verbose_name="Ссылка на livelib", blank=True)

    def __str__(self):
        return str(self.title) + " (" + str(self.author) + ")"

    def equals(self, example):
        return (str(self.title) + " (" + str(self.author) + ")") == example

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'
        ordering = ['title']
