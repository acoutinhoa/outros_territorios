# Generated by Django 2.0.8 on 2018-11-08 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0012_auto_20181106_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fim', models.DateTimeField()),
            ],
        ),
    ]
