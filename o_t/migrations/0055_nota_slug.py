# Generated by Django 2.0.8 on 2018-10-16 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0054_nota_slug_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='nota',
            name='slug',
            field=models.SlugField(blank=True, max_length=210, null=True, unique=True),
        ),
    ]