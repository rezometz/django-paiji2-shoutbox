# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=200, verbose_name='message')),
                ('posted_at', models.DateTimeField(auto_now_add=True, verbose_name='publication date')),
                ('author', models.ForeignKey(related_name='notes', verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-posted_at',),
                'verbose_name': 'note',
                'verbose_name_plural': 'notes',
            },
        ),
    ]
