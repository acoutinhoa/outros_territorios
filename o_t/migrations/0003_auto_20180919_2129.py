# Generated by Django 2.0.8 on 2018-09-20 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0002_nota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nota',
            name='data0',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='nota',
            name='data1',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
