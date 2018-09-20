from django.db import models
from django.utils import timezone
from datetime import date

class Cartaz(models.Model):
	titulo = models.CharField(max_length=200,)
	datas = models.TextField(blank=True)
	texto = models.TextField(blank=True)
	imagens = models.ManyToManyField('Imagem', blank=True)
	def __str__(self):
		return self.titulo

class Imagem(models.Model):
	nome = models.CharField(max_length=200)
	img = models.ImageField(upload_to = 'o_t/img/')
	def __str__(self):
		return self.nome

class Nota(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    titulo = models.CharField('título', max_length=200)
    # slug = models.SlugField(max_length=200, unique=True, blank=True)
    texto = models.TextField()
    data0 = models.DateTimeField(auto_now_add=True)
    data1 = models.DateTimeField(blank=True, null=True)
    imagem = models.ImageField(upload_to = 'o_t/blog/', blank=True)
    def publish(self):
        self.data1 = timezone.now()
        self.save()
    def __str__(self):
        return self.titulo
