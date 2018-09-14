from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField('título', max_length=200)
    text = models.TextField('texto')
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title

class Resumo(models.Model):
	titulo = models.CharField('título', max_length=200)
	subtitulo = models.TextField('datas', blank=True)
	resumo = models.TextField('resumo', blank=True)
	imgs = models.ManyToManyField('Imagem', blank=True)
	def __str__(self):
		return self.titulo

class Imagem(models.Model):
	nome = models.CharField('nome', max_length=200)
	img = models.ImageField(upload_to = 'blog/img/')
	def __str__(self):
		return self.nome

