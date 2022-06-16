from django.contrib import admin

from .models import Book, BookGenre


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'updated_at', 'is_published')
    list_display_links = ('book_id', 'title')
    search_fields = ('title', 'author')


class BookGenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(BookGenre, BookGenreAdmin)
admin.site.register(Book, BookAdmin)
