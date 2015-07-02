# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.contrib.djangoitem import DjangoItem
from books.models import Book, Category, Chapter, Reader


class BookItem(DjangoItem):
    django_model = Book


class BookCategoryItem(DjangoItem):
    django_model = Category


class BookChapterItem(DjangoItem):
    django_model = Chapter


class BookReaderItem(DjangoItem):
    django_model = Reader
