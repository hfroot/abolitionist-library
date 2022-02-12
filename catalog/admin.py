from django.contrib import admin
from .models import Tag, Book
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)

"""Minimal registration of Models.
admin.site.register(Book)
admin.site.register(Tag)
"""

admin.site.register(Tag)


class BooksInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Book


class BookAdmin(admin.ModelAdmin):
    """Administration object for Book models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of book instances in book view (inlines)
    """
    list_display = ('title', 'author', 'display_tag')


admin.site.register(Book, BookAdmin)
