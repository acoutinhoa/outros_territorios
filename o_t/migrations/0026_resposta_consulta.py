# Generated by Django 2.0.8 on 2018-09-26 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0025_auto_20180926_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='resposta',
            name='consulta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='o_t.Pergunta'),
        ),
    ]