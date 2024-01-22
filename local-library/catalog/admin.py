from django.contrib import admin

from .models import Genre, Book, BookInstance, Author, Language


class BookInline(admin.TabularInline):
    
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    
    list_display = ['last_name', 'first_name', 'date_of_birth', 'date_of_death']
    list_filter = ['date_of_death']
    search_fields = ['last_name', 'first_name']

    inlines = [BookInline]


class BookInstanceInline(admin.TabularInline):
    
    model = BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    
    list_display = ['title', 'author', 'language', 'display_genres']
    list_filter = ['language', 'genre']
    search_fields = ['title', 'author']
    
    inlines = [BookInstanceInline]

    def display_genres(self, instance):
        return [genre.name for genre in instance.genre.all()]
    display_genres.short_description = 'Жанры'


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):

    list_display = ['id', 'book', 'borrower', 'status', 'due_back']
    list_filter = ['status', 'due_back']
    search_fields = ['book', 'id']
    
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Доступность', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    
    list_display = ['name']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    
    list_display = ['name']