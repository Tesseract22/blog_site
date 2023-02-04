# Generated by Django 3.2.15 on 2022-11-13 04:22

import article.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_article_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.ImageField(default='img/article_default.jpg', upload_to=article.models.Article.cover_location),
        ),
    ]
