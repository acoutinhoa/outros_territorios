# Generated by Django 2.0.8 on 2018-10-18 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0059_auto_20181017_1323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nota',
            options={'ordering': ['-data1', '-data0']},
        ),
        migrations.AlterField(
            model_name='nota',
            name='data1',
            field=models.DateTimeField(blank=True, null=True, verbose_name='publicação'),
        ),
    ]