# Generated by Django 2.0.8 on 2018-10-24 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0004_blocorespostas_faq_pergunta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inscricao',
            name='termos',
        ),
    ]