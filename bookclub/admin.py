from django.contrib import admin
from .models import Genre, Book, BookReview, Bookmark, Borrow


class BookInLine(admin.StackedInline):
    model = Book


class BookReviewInline(admin.TabularInline):
    model = BookReview


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [
        BookInLine,
    ]


class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = ("title", "author", "publication_year")
    list_display = (
        "title",
        "genre",
        "author",
        "publication_year",
        "available_to_borrow",
        "created_on",
        "updated_on",
    )
    list_filter = (
        "genre",
        "available_to_borrow",
        "publication_year",
    )
    fieldsets = [
        ("Basic Info", {"fields": [("title", "genre", "author")]}),
        (
            "Details",
            {
                "fields": [
                    (
                        "synopsis",
                        "publication_year",
                        "available_to_borrow",
                        "contributor",
                    )
                ]
            },
        ),
    ]

    inlines = [BookReviewInline]


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user_reviewer", "anon_reviewer", "title")
    search_fields = ("title",)
    list_filter = ("book",)


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("profile", "book", "date_bookmarked")
    list_filter = ("date_bookmarked",)
    search_fields = ("profile__user__username", "book__title")


class BorrowAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "borrower",
        "name",
        "date_borrowed",
        "date_to_return",
    )
    list_filter = ("date_borrowed", "date_to_return")
    search_fields = ("name", "book__title", "borrower__user__username")


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Borrow, BorrowAdmin)
