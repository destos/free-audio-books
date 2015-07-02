# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import sizefield.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('author_url', models.URLField(max_length=255)),
                ('years', models.CharField(max_length=255)),
                ('book_url', models.URLField(max_length=255)),
                ('book_cover', models.URLField(max_length=255)),
                ('zip_url', models.URLField(max_length=255)),
                ('zip_size', sizefield.models.FileSizeField()),
                ('total_time', models.TimeField()),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, db_index=True)),
                ('lv_pk', models.PositiveSmallIntegerField(help_text=b'LibriVox specific ID', unique=True, db_index=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='books.Category', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('number', models.PositiveSmallIntegerField()),
                ('time', models.TimeField()),
                ('mp3_url', models.URLField(max_length=255)),
                ('mp3_size', sizefield.models.FileSizeField()),
                ('book', models.ForeignKey(related_name='chapters', to='books.Book')),
            ],
            options={
                'ordering': ('-book', '-number'),
                'verbose_name': 'Chapter',
                'verbose_name_plural': 'Chapters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chapter',
            name='reader',
            field=models.ForeignKey(related_name='read_chapters', blank=True, to='books.Reader', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(related_name='books', to='books.Category'),
            preserve_default=True,
        ),
    ]
