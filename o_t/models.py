from django.db import models
from django.utils import timezone
from datetime import date
from django.utils.text import slugify
import uuid, random

class Cartaz(models.Model):
	pagina = models.CharField(max_length=50)
	titulo = models.TextField(blank=True)
	datas = models.TextField(blank=True)
	texto = models.TextField(blank=True)
	def __str__(self):
		return self.pagina

def arquivos_filepath(instance, filename):
    return 'o_t/arquivos/{0}/{1}'.format(instance.pagina, filename)


class Arquivo(models.Model):
	tipos = [
		('o_t','o_t'),
		('patrocinio','patrocinio'),
	]
	pagina = models.ForeignKey(Cartaz, on_delete=models.CASCADE, blank=True)
	tipo = models.CharField(max_length=20, choices=tipos, blank=True, null=True)
	nome = models.CharField(max_length=200, blank=True)
	arquivo = models.FileField(upload_to = arquivos_filepath)
	def __str__(self):
		return self.nome
	def save(self, *args, **kwargs):
		self.nome = self.arquivo.name.split('.')[0]
		super().save(*args, **kwargs)

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
	return str(BlocoRespostas.objects.get_or_create(nome='rascunho')[0].pk)

class Pergunta(models.Model):
	bloco = models.ForeignKey(BlocoRespostas, on_delete=models.SET(set_rascunho), blank=True, default=set_rascunho)
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
	areas = [
		('arquitetura','Arquitetura'),
		('artesV','Artes Visuais'),
		('artesP','Artes Performáticas'),
		('design','Design'),
		('paisagismo','Paisagismo'),
	]
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	data0 = models.DateTimeField(auto_now_add=True)
	email = models.EmailField(unique=True)
	nome = models.CharField(max_length=30)
	sobrenome = models.CharField(max_length=70, null=True)
	area = models.CharField('área', choices=areas, max_length=20)
	termos = models.BooleanField()
	codigo = models.CharField(max_length=5, unique=True, blank=True, null=True)
	ok = models.BooleanField(default=False)

	def __str__(self):
		return self.nome
	class Meta:
		ordering = ['data0']
	def novo_codigo(self):
		codigo = str(random.randint(10000,99999))
		if Inscricao.objects.filter(codigo=codigo).exists():
			self.novo_codigo()
		return codigo
	def save(self, *args, **kwargs):
		if not self.codigo:
			self.codigo = self.novo_codigo()
		super().save(*args, **kwargs)


class Dados(models.Model):
	inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE)

	nascimento = models.DateField()
	cpf = models.CharField('CPF/CNPJ', max_length=30, unique=True)
	celular = models.CharField(max_length=20)

	rua = models.CharField('endereço', max_length=60)
	complemento = models.CharField(max_length=20, blank=True)
	bairro = models.CharField(max_length=20)
	cidade = models.CharField(max_length=20)
	estado = models.CharField(max_length=2)
	cep = models.CharField('CEP', max_length=15)
	pais = models.CharField(max_length=20)

	def __str__(self):
		return self.inscricao.nome

class Equipe(models.Model):
	inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE)
	nome = models.CharField(max_length=30)
	sobrenome = models.CharField(max_length=70, null=True)
	email = models.EmailField('e-mail')

	def __str__(self):
		return self.nome

def inscricao_filepath(instance, filename):
    return 'o_t/concuso/{0}/{1}'.format(instance.inscricao.id, filename)

class Projeto(models.Model):
	palafitas = [
		('01', '01. Cônsul Walter 425: palafita-pomar'),
		('02', '02. Cônsul Walter 437: palafita-caverna'),
		('03', '03. Cônsul Walter 483: palafita-empena'),
		('04', '04. Cônsul Walter 511: palafita-indiscreta'),
		('05', '05. Teresa Mota Valadares 76: palafita-caleidoscópica'),
		('06', '06. Fidélis Martins 173: palafita-esbelta'),
		('07', '07. Maria Heilbuth Surete 1223: palafita-dos-cachorros'),
		('08', '08. Maria Heilbuth Surete 1159: palafita-comum'),
		('09', '09. Maria Heilbuth Surete 1193: palafita-gigante-I'),
		('10', '10. Maria Heilbuth Surete 1295: palafita-gigante-II'),
	]
	inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE)
	slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
	palafita = models.CharField(choices=palafitas, max_length=2)
	nome = models.CharField('título', max_length=200, blank=True)
	texto = models.TextField('descrição', blank=True, max_length=3000)
	img = models.ImageField('imagem principal', upload_to = inscricao_filepath, blank=True)
	arquivo = models.FileField(upload_to = inscricao_filepath, blank=True)
	def __str__(self):
		return self.nome
