# Generated by Django 2.0.8 on 2018-09-20 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0005_nota'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartaz',
            name='imagens',
        ),
        migrations.DeleteModel(
            name='Cartaz',
        ),
        migrations.DeleteModel(
            name='Imagem',
        ),
    ]
