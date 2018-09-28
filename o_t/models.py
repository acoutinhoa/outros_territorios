from django.db import models
from django.utils import timezone
from datetime import date
from django.utils.text import slugify
import uuid

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

class BlocoRespostas(models.Model):
	nome = models.CharField(max_length=30)
	slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
	data0 = models.DateTimeField(auto_now_add=True)
	data1 = models.DateTimeField(blank=True, null=True)
	def publish(self):
		self.data1 = timezone.now()
		self.save()
	def __str__(self):
		return self.nome

def set_rascunho():
	return str(BlocoRespostas.objects.get(nome='rascunho').pk)

class Pergunta(models.Model):
	# bloco = models.ForeignKey(BlocoRespostas, on_delete=models.SET(set_rascunho), blank=True, default=set_rascunho)
	bloco = models.ForeignKey(BlocoRespostas, on_delete=models.CASCADE, blank=True, null=True)
	nome = models.CharField(max_length=100)
	email = models.EmailField()
	consulta = models.TextField()
	pergunta = models.TextField(blank=True, null=True)
	resposta = models.TextField(blank=True, null=True)
	data = models.DateTimeField()
	def __str__(self):
		return self.pk
	class Meta:
		ordering = ['-data']

class Faq(models.Model):
	pergunta = models.TextField()
	resposta = models.TextField()
	data0 = models.DateTimeField(auto_now_add=True)
	publicar = models.BooleanField(default=False)
	def __str__(self):
		return self.pergunta
	class Meta:
		ordering = ['data0']

class Inscricao(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	data0 = models.DateTimeField(auto_now_add=True)
	nome = models.CharField(max_length=100)
	email = models.EmailField('e-mail', unique=True)
	area = models.CharField('área de atuação profissional', max_length=50)
	termos = models.BooleanField()

	def __str__(self):
		return self.nome
	class Meta:
		ordering = ['data0']


class Dados(models.Model):
	inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE)

	nascimento = models.DateField()
	cpf = models.CharField('CPF', max_length=11, unique=True)
	rg = models.CharField('RG', max_length=15)
	celular = models.CharField(max_length=13)

	cep = models.CharField('CEP', max_length=8)
	rua = models.CharField(max_length=60)
	complemento = models.CharField(max_length=20, blank=True)
	bairro = models.CharField(max_length=20)
	cidade = models.CharField(max_length=20)
	estado = models.CharField(max_length=2)
	pais = models.CharField(max_length=20)

	def __str__(self):
		return self.inscricao.nome

class Equipe(models.Model):
	inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE)
	nome = models.CharField(max_length=100)
	email = models.EmailField('e-mail')

	def __str__(self):
		return self.nome

def inscricao_filepath(instance, filename):
    return 'concuso/{0}/{1}'.format(instance.inscricao.id, filename)

class Projeto(models.Model):
	inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE)
	nome = models.CharField('titulo do projeto', max_length=200, blank=True)
	slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
	img = models.ImageField('imagem principal', upload_to = inscricao_filepath, blank=True)
	texto = models.TextField('descrição do projeto', blank=True)

	def __str__(self):
		return self.nome

class Prancha(models.Model):
	inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE)
	img = models.ImageField('prancha', upload_to = inscricao_filepath)

	def __str__(self):
		return '%s_%s' % (self.inscricao.nome, self.pk)
