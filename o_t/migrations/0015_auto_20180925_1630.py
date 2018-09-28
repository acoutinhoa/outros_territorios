# Generated by Django 2.0.8 on 2018-09-25 19:30

from django.db import migrations, models
import django.db.models.deletion
import o_t.models


class Migration(migrations.Migration):

    dependencies = [
        ('o_t', '0014_auto_20180925_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prancha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=o_t.models.inscricao_filepath, verbose_name='prancha')),
                ('inscricao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='o_t.Inscricao')),
            ],
        ),
        migrations.AddField(
            model_name='projeto',
            name='img',
            field=models.ImageField(blank=True, upload_to=o_t.models.inscricao_filepath, verbose_name='imagem principal'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='bairro',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='dados',
            name='celular',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='dados',
            name='cep',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='dados',
            name='cidade',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='dados',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='estado',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='dados',
            name='nascimento',
            field=models.DateField(blank=True, verbose_name='data de nascimento'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='rg',
            field=models.CharField(blank=True, max_length=20, verbose_name='RG'),
        ),
        migrations.AlterField(
            model_name='dados',
            name='rua',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='equipe',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='e-mail'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='nome',
            field=models.CharField(blank=True, max_length=200, verbose_name='titulo do projeto'),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='texto',
            field=models.TextField(blank=True, verbose_name='descrição do projeto'),
        ),
    ]
