# Generated by Django 2.0.8 on 2018-10-03 19:47

from django.db import migrations, models
import o_t.models


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0035_auto_20180928_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='arquivo',
            name='tipo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='arquivo',
            name='arquivo',
            field=models.FileField(upload_to=o_t.models.arquivos_filepath),
        ),
    ]
