# Generated by Django 2.0.8 on 2018-10-15 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0047_auto_20181015_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='pergunta',
            name='pergunta_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pergunta',
            name='resposta_en',
            field=models.TextField(blank=True, null=True),
        ),
    ]