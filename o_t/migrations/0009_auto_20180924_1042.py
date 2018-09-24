# Generated by Django 2.0.8 on 2018-09-24 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0008_juri'),
    ]

    operations = [
        migrations.AddField(
            model_name='juri',
            name='site',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='arquivo',
            name='pagina',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='o_t.Cartaz'),
        ),
    ]
