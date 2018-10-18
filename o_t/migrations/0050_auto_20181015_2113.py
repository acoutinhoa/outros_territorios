# Generated by Django 2.0.8 on 2018-10-16 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0049_auto_20181015_2108'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='arquivo',
            options={'ordering': ['tipo']},
        ),
        migrations.AlterField(
            model_name='arquivo',
            name='tipo',
            field=models.CharField(blank=True, choices=[('01', 'o_t'), ('02', 'organização'), ('03', 'patrocínio'), ('04', 'apoio')], max_length=20, null=True),
        ),
    ]
