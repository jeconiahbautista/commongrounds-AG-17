from django.contrib import admin
from .models import Genre, Book

class BookInLine(admin.TabularInline):
    model = Book

class GenreAdmin(admin.ModelAdmin):
    inlines = Genre
    inlines = []

class BookAdmin(admin.ModelAdmin):
    model = Book

admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)

# Register your models here.
