from django.contrib import admin
from .models import Genre, Book

"""Minimal registration of Models.
admin.site.register(Book)
admin.site.register(Genre)
"""

admin.site.register(Genre)


class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book


class BookAdmin(admin.ModelAdmin):
    """Administration object for Book models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of book instances in book view (inlines)
    """
    list_display = ('title', 'author', 'display_genre')


admin.site.register(Book, BookAdmin)
