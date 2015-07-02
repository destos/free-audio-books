from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from . import models


class ChapterInline(admin.TabularInline):
    model = models.Chapter
    extra = 0
    fields = ('number', 'name', 'time',)
    can_delete = False


class BookAdmin(admin.ModelAdmin):
    model = models.Book
    inlines = (ChapterInline, )
    fields = ('name', 'description', 'author', 'author_url', 'years', 'book_url',
              'book_cover', 'zip_url', 'zip_size', 'categories', 'total_time')
    # list_display = ('behavior', 'verb', 'name', 'approved',)
    # readonly_fields = ('slug', 'creator', 'created', 'modified',)


class CategoryAdmin(DjangoMpttAdmin):
    model = models.Category


admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Category, CategoryAdmin)
