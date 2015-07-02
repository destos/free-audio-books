from django.db import models
from sizefield.models import FileSizeField

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=255, db_index=True)
    lv_pk = models.PositiveSmallIntegerField(
        unique=True, db_index=True, help_text='LibriVox specific ID')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    will_scrape = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ('lv_pk',)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=255)
    # TODO, turn author into a model
    author = models.CharField(max_length=255)
    author_url = models.URLField(max_length=255)
    years = models.CharField(max_length=255)
    book_url = models.URLField(max_length=255)
    book_cover = models.URLField(max_length=255)
    zip_url = models.URLField(max_length=255)
    zip_size = FileSizeField()
    # Genres and subjects on LibriVox
    categories = models.ManyToManyField(Category, related_name='books')
    total_time = models.TimeField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __unicode__(self):
        return self.name


class Reader(models.Model):
    name = models.CharField(max_length=255)
    lv_pk = models.PositiveSmallIntegerField(
        unique=True, db_index=True, help_text='LibriVox specific ID')


class Chapter(models.Model):
    name = models.CharField(max_length=255)
    number = models.PositiveSmallIntegerField()
    time = models.TimeField()
    book = models.ForeignKey(Book, related_name='chapters')
    reader = models.ForeignKey(Reader, related_name='read_chapters', blank=True, null=True)
    mp3_url = models.URLField(max_length=255)
    mp3_size = FileSizeField()
    language = models.CharField(default='en', max_length=20)

    class Meta:
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'
        ordering = ('-book', '-number',)


# TODO
# class BookGroups(models.Model):
#     pass
