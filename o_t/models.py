from django.db import models
from django.utils import timezone
from datetime import date

class Cartaz(models.Model):
	pagina = models.CharField(max_length=50)
	titulo = models.TextField(blank=True)
	datas = models.TextField(blank=True)
	texto = models.TextField(blank=True)
	def __str__(self):
		return self.pagina

class Arquivo(models.Model):
	pagina = models.ForeignKey(Cartaz, on_delete=models.CASCADE, blank=True)
	nome = models.CharField(max_length=200)
	arquivo = models.FileField(upload_to = 'o_t/arquivos/')
	def __str__(self):
		return self.nome

class Nota(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    titulo = models.CharField('título', max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    texto = models.TextField()
    data0 = models.DateTimeField(auto_now_add=True)
    data1 = models.DateTimeField(blank=True, null=True)
    imagem = models.ImageField(upload_to = 'o_t/blog/', blank=True)
    def publish(self):
        self.data1 = timezone.now()
        self.save()
    def __str__(self):
        return self.titulo

class Juri(models.Model):
	nome = models.CharField(max_length=200)
	site = models.URLField(blank=True)
	bio = models.TextField()
	def __str__(self):
		return self.nome


