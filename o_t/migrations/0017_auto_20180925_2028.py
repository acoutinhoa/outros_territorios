# Generated by Django 2.0.8 on 2018-09-25 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0016_auto_20180925_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dados',
            name='inscricao',
        ),
        migrations.DeleteModel(
            name='Dados',
        ),
    ]