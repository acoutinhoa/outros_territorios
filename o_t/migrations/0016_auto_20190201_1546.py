# Generated by Django 2.0.8 on 2019-02-01 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0015_auto_20190131_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selecao',
            name='inscricao',
        ),
        migrations.AddField(
            model_name='inscricao',
            name='ok',
            field=models.CharField(choices=[('-', '---'), ('ok', 'aprovado'), ('no', 'reprovado')], default='-', max_length=2, verbose_name='pré-seleção'),
        ),
        migrations.AddField(
            model_name='inscricao',
            name='texto',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='inscricao',
            name='texto_en',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='inscricao',
            name='titulo',
            field=models.CharField(blank=True, max_length=220),
        ),
        migrations.AddField(
            model_name='inscricao',
            name='titulo_en',
            field=models.CharField(blank=True, max_length=220),
        ),
        migrations.DeleteModel(
            name='Selecao',
        ),
    ]