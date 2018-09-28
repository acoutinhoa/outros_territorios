# Generated by Django 2.0.8 on 2018-09-26 23:47

from django.db import migrations, models
import o_t.models


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0032_remove_resposta_consulta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pergunta',
            name='ok',
        ),
        migrations.AddField(
            model_name='pergunta',
            name='bloco',
            field=models.ForeignKey(blank=True, default=o_t.models.set_rascunho, on_delete=models.SET(o_t.models.set_rascunho), to='o_t.BlocoRespostas'),
        ),
        migrations.AddField(
            model_name='pergunta',
            name='resposta',
            field=models.TextField(blank=True, null=True),
        ),
    ]