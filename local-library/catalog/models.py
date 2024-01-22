import uuid

from django.db import models
from django.urls import reverse
from datetime import date
from django.conf import settings


class Genre(models.Model):
    
    name = models.CharField(verbose_name='Название жанра', max_length=200, unique=True, help_text='Название жанра (Научная фантастик, психология и т.п.)')
    
    
    def __str__(self) -> str:
        
        return self.name
    
    def get_absolute_url(self) -> str:

        return reverse('genre-detail', args=[str(self.id)])
    
    
    class Meta:
        
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    

class Book(models.Model):
    
    title = models.CharField(verbose_name='Название книги', max_length=200, help_text='Название книги')
    summary = models.TextField(verbose_name='Описание', max_length=1500, help_text='Краткое описание книги')
    isbn = models.CharField(verbose_name='ISBN', max_length=25, help_text='13-ти символьный <a href="https://www.isbn-international.org/content/what-isbn''">ISBN номер</a>')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', help_text='Жанры, к которым относится книга')
    
    language = models.ForeignKey('Language', verbose_name='Язык', on_delete=models.DO_NOTHING, help_text='Язык, на котором написана книга')
    author = models.ForeignKey('Author', verbose_name='Автор', on_delete=models.SET_NULL, null=True, help_text='Автор книги')
    
    
    def __str__(self) -> str:
        
        return self.title
    
    def get_absolute_url(self) -> str:
        
        return reverse('book-detail', args=[str(self.id)])
    
    
    class Meta:
        
        ordering = ['author', 'title', 'language']
        verbose_name = 'Книгу'
        verbose_name_plural = 'Книги'
    
    
class BookInstance(models.Model):
    
    id = models.UUIDField(primary_key=True, verbose_name='UUID', default=uuid.uuid4, help_text='Уникальный идентификатор экземпляря книги')
    imprint = models.CharField(verbose_name='Издание', max_length=200, help_text='Дата издания книги, издатель и т.п.')
    due_back = models.DateField(verbose_name='Дата возрата', null=True, blank=True, help_text='Дата, когда экземпляр должен быть возвращен')
    
    book = models.ForeignKey('Book', verbose_name='Книга', on_delete=models.RESTRICT, null=True, help_text='Книга, к которой относится экземпляр')
    
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Владелец', on_delete=models.SET_NULL, null=True, blank=True, help_text='Человек, который забрал экземпляр')
    
    
    LOAN_STATUS = (
        ('m', 'На обслуживании'),
        ('o', 'Выдан'),
        ('a', 'Доступен'),
        ('r', 'Забронирован')
    )
    
    status = models.CharField(verbose_name='Статус экземпляра', max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Доступность экземпляр')
    
    
    class Meta:
        
        ordering = ['book', 'due_back']
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'
        permissions = (("can_mark_returned", "Set book as returned"),)
        
    
    def get_absolute_url(self) -> str:

        return reverse('bookinstance-detail', args=[str(self.id)])
    
    def __str__(self) -> str:
        
        return '%s (%s)' % (self.id, self.book.title)
    
    @property
    def is_overdue(self):
        
        return bool(self.due_back and date.today() > self.due_back)
    

class Author(models.Model):
    
    first_name = models.CharField(verbose_name='Имя', max_length=100, help_text='Имя и отчество (опционально) автора')
    last_name = models.CharField(verbose_name='Фамилия', max_length=100, help_text='Фамилия автора')
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True, blank=True, help_text='Дата рождения автора')
    date_of_death = models.DateField(verbose_name='Дата смерти', null=True, blank=True, help_text='Дата смерти автора')
    
    
    class Meta:

        ordering = ['last_name', 'first_name']
        verbose_name = 'Автора'
        verbose_name_plural = 'Авторы'

    
    def get_absolute_url(self):
        
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self) -> str:
        
        return '%s, %s' % (self.last_name, self.first_name)
   

class Language(models.Model):
    
    name = models.CharField(verbose_name='Язык', max_length=100, unique=True, help_text='Язык, на котором написан оригинал')
    
    
    class Meta:
        
        ordering = ['name']
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'
    
    
    def get_absolute_url(self) -> str:

        return reverse('language-detail', args=[str(self.id)])
    
    def __str__(self) -> str:
        
        return '%s' % (str(self.name))