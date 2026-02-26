from django.contrib import admin
from .models import Genre, Book

class BookInLine(admin.StackedInline):
    model = Book

class GenreAdmin(admin.ModelAdmin):
    model = Genre
    inlines = [BookInLine,]

class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = ('title', 'author', 'publication_year')
    list_display = ('title', 'genre', 'author', 'publication_year', 'created_on', 'updated_on')
    list_filter = ('genre',)
    fieldsets = [
        ('Details', {
            'fields': [
                ('title', 'genre', 'author', 'publication_year',)
            ]
        })
    ]

admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)