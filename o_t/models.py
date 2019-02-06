from django.db import models
from django.utils import timezone
from django.urls import reverse
from datetime import date
from django.utils.text import slugify
import uuid, random
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from django_countries import countries

class Cartaz(models.Model):
	pagina = models.CharField(max_length=20)
	titulo = models.TextField(blank=True)
	datas = models.TextField(blank=True)
	texto = models.TextField(blank=True)
	titulo_en = models.TextField(blank=True)
	datas_en = models.TextField(blank=True)
	texto_en = models.TextField(blank=True)
	def __str__(self):
		return self.pagina

def arquivos_filepath(instance, filename):
    return 'o_t/arquivos/{0}/{1}'.format(instance.pagina, filename)

class Arquivo(models.Model):
	tipos = [
		('01','o_t'),
		('02',_('organização')),
		('03',_('patrocínio')),
		('04',_('apoio institucional')),
		('05',_('parceiro de mídia')),
	]
	pagina = models.ForeignKey(Cartaz, on_delete=models.CASCADE, blank=True)
	nome = models.CharField(max_length=200, blank=True)
	arquivo = models.FileField(upload_to = arquivos_filepath, blank=True, null=True)
	en = models.BooleanField(default=False)
	imagem = models.ImageField(upload_to = arquivos_filepath, blank=True, null=True)
	tipo = models.CharField(max_length=20, choices=tipos, blank=True, null=True)
	altura = models.CharField(max_length=4, default='100')
	link = models.URLField(blank=True)
	def __str__(self):
		return '%s_%s' % (self.pagina, self.nome)
	def save(self, *args, **kwargs):
		if not self.nome:
			if self.arquivo:
				self.nome = self.arquivo.name
			elif self.imagem:
				self.nome = self.imagem.name.split('.')[0]
		super().save(*args, **kwargs)
	def tipo_verbose(self):
	        return dict(Arquivo.tipos)[self.tipo]
	class Meta:
		ordering = ['tipo']

class Tag(models.Model):
	tag = models.SlugField(max_length=100, unique=True)
	tag_en = models.SlugField(max_length=100, unique=True)
	def __str__(self):
		return self.tag
	class Meta:
		ordering = ['tag']

class Nota(models.Model):
	autor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	titulo = models.CharField('título', max_length=200)
	titulo_en = models.CharField(max_length=200, blank=True)
	slug = models.SlugField(max_length=220, blank=True, null=True, unique=True)
	slug_en = models.SlugField(max_length=220, blank=True, null=True, unique=True)
	texto = models.TextField()
	texto_en = models.TextField(blank=True)
	data0 = models.DateTimeField(auto_now_add=True)
	data1 = models.DateTimeField('publicação', blank=True, null=True)
	tags = models.ManyToManyField(Tag, blank=True)
	
	def publish(self):
		self.data1 = timezone.now()
		self.save()
	def __str__(self):
		return self.titulo
	def criar_slug(self, lang='pt', car=''):
		if lang == 'pt':
			slug = slugify(self.titulo)+car
			nota = Nota.objects.filter(slug=slug)
		elif lang == 'en':
			slug = slugify(self.titulo_en)+car
			nota = Nota.objects.filter(slug_en=slug)
		if nota.exists() and nota[0] != self:
			car += '-'
			slug = self.criar_slug(lang=lang, car=car)
		return slug
	def save(self, *args, **kwargs):
		if not self.autor:
			nota.autor = request.user
		if not self.slug:
			self.slug = self.criar_slug()
		if self.titulo_en and not self.slug_en:
			self.slug_en = self.criar_slug(lang='en')
		super().save(*args, **kwargs)
	class Meta:
		ordering = ['-data1']
	def get_absolute_url(self):
		if get_language() == 'en' and self.slug_en:
			slug = self.slug_en
		else:
			slug = self.slug
		return reverse('blog_slug', args=[slug])

def imagem_filepath(instance, filename):
    return 'o_t/blog/{0}/{1}'.format(instance.nota.pk, filename)

class Imagem(models.Model):
	nota = models.ForeignKey(Nota, on_delete=models.CASCADE)
	nome = models.CharField(max_length=200, blank=True)
	arquivo = models.ImageField(upload_to = imagem_filepath)
	def __str__(self):
		return self.nome
	def save(self, *args, **kwargs):
		if not self.nome:
			self.nome = self.arquivo.name.split('.')[0]
		super().save(*args, **kwargs)

class Juri(models.Model):
	nome = models.CharField(max_length=200)
	site = models.URLField(blank=True)
	bio = models.TextField()
	bio_en = models.TextField(blank=True)
	def __str__(self):
		return self.nome
	class Meta:
		ordering = ['nome']

class BlocoRespostas(models.Model):
	nome = models.CharField(max_length=30)
	nome_en = models.CharField(max_length=30, blank=True)
	slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
	slug_en = models.SlugField(max_length=200, blank=True, null=True, unique=True)
	data0 = models.DateTimeField(auto_now_add=True)
	data1 = models.DateTimeField(blank=True, null=True)
	def publish(self):
		self.data1 = timezone.now()
		self.save()
	def criar_slug(self, lang='pt', car=''):
		if lang == 'pt':
			slug = slugify(self.nome)+car
			bloco = BlocoRespostas.objects.filter(slug=slug)
		elif lang == 'en':
			slug = slugify(self.nome_en)+car
			bloco = BlocoRespostas.objects.filter(slug_en=slug)
		if bloco.exists() and bloco[0] != self:
			car += '-'
			slug = self.criar_slug(lang=lang, car=car)
		return slug
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self.criar_slug()
		if self.nome_en and not self.slug_en:
			self.slug_en = self.criar_slug(lang='en')
		super().save(*args, **kwargs)
	def __str__(self):
		return self.nome

def set_rascunho():
	return str(BlocoRespostas.objects.get_or_create(nome='rascunho')[0].pk)

class Pergunta(models.Model):
	bloco = models.ForeignKey(BlocoRespostas, on_delete=models.SET(set_rascunho), blank=True, default=set_rascunho)
	nome = models.CharField(_('nome'), max_length=100)
	email = models.EmailField('e-mail')
	consulta = models.TextField(_('consulta'),)
	pergunta = models.TextField(blank=True, null=True)
	pergunta_en = models.TextField(blank=True, null=True)
	resposta = models.TextField(blank=True, null=True)
	resposta_en = models.TextField(blank=True, null=True)
	data = models.DateTimeField(auto_now_add=True)
	lang = models.CharField(max_length=5)
	def __str__(self):
		return self.nome
	class Meta:
		ordering = ['-data']

class Faq(models.Model):
	pergunta = models.TextField()
	resposta = models.TextField()
	pergunta_en = models.TextField(blank=True)
	resposta_en = models.TextField(blank=True)
	data0 = models.DateTimeField(auto_now_add=True)
	publicar = models.BooleanField(default=False)
	def __str__(self):
		return self.pergunta
	class Meta:
		ordering = ['data0']

class Data(models.Model):
	fim=models.DateTimeField()

class Inscricao(models.Model):
	areas = [
		('01',_('Arquitetura')),
		('02',_('Artes Visuais')),
		('03',_('Artes Performáticas')),
		('04',_('Design')),
		('05',_('Paisagismo')),
	]
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	data0 = models.DateTimeField(auto_now_add=True)
	email = models.EmailField('e-mail', unique=True)
	nome = models.CharField(_('nome'), max_length=30)
	sobrenome = models.CharField(_('sobrenome'), max_length=70, null=True)
	area = models.CharField(_('área'), choices=areas, max_length=20)
	codigo = models.CharField(max_length=5, unique=True, blank=True, null=True)
	finalizada = models.DateTimeField(blank=True, null=True)
	# selecao
	ok = models.CharField('pré-seleção', choices=[('-', '---'), ('ok','aprovado'),('no','reprovado')], max_length=2, default='-')
	traducao = models.CharField('tradução', choices=[('-', '---'), ('pt','português'),('en','inglês')], max_length=2, default='-')
	titulo = models.CharField(max_length=220, blank=True)
	texto = models.TextField(blank=True)
	media = models.FloatField(default=0)
	s2 = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return '%s - %s' % (self.nome, self.email)
	class Meta:
		ordering = ['finalizada', 'data0']
	def finaliza(self):
		self.finalizada = timezone.now()
		self.save()
	def novo_codigo(self):
		codigo = str(random.randint(10000,99999))
		if Inscricao.objects.filter(codigo=codigo).exists():
			codigo = self.novo_codigo()
		return codigo
	def save(self, *args, **kwargs):
		if not self.codigo:
			self.codigo = self.novo_codigo()
		super().save(*args, **kwargs)
	def select_verbose(self):
		return dict(Inscricao.areas)[self.area]


class Dados(models.Model):
	inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE)

	nascimento = models.DateField(_('nascimento'), )
	cpf = models.CharField(_('CPF/CNPJ'), max_length=30, unique=True)
	celular = models.CharField(_('celular'), max_length=20)

	pais = CountryField(_('país'), default='BR')
	rua = models.CharField(_('endereço'), max_length=100)
	complemento = models.CharField(_('complemento'), max_length=20, blank=True)
	cidade = models.CharField(_('cidade'), max_length=50)
	estado = models.CharField(_('estado'), max_length=4,)
	cep = models.CharField(_('CEP'), max_length=15)

	def __str__(self):
		return self.inscricao.nome
	def select_verbose(self):
		return dict(countries)[self.pais]

class Equipe(models.Model):
	inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE)
	nome = models.CharField(_('nome'), max_length=30)
	sobrenome = models.CharField(_('sobrenome'), max_length=70, null=True)
	email = models.EmailField('e-mail')

	def __str__(self):
		return self.nome

def inscricao_filepath(instance, filename):
    return 'o_t/concurso/{0}/{1}'.format(instance.inscricao.id, filename)

def validate_size(value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('Erro: o arquivo não deve ultrapassar 10MB'))

class Projeto(models.Model):
	palafitas = [
		('01', _('01. Cônsul Walter 425: palafita-pomar')),
		('02', _('02. Cônsul Walter 437: palafita-caverna')),
		('03', _('03. Cônsul Walter 483: palafita-empena')),
		('04', _('04. Cônsul Walter 511: palafita-indiscreta')),
		('05', _('05. Teresa Mota Valadares 76: palafita-caleidoscópica')),
		('06', _('06. Fidélis Martins 173: palafita-esbelta')),
		('07', _('07. Maria Heilbuth Surete 1223: palafita-dos-cachorros')),
		('08', _('08. Maria Heilbuth Surete 1159: palafita-comum')),
		('09', _('09. Maria Heilbuth Surete 1193: palafita-gigante-I')),
		('10', _('10. Maria Heilbuth Surete 1295: palafita-gigante-II')),
	]
	inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE)
	slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
	palafita = models.CharField(_('palafita'), choices=palafitas, max_length=2, blank=True)
	nome = models.CharField(_('título'), max_length=200, blank=True)
	texto = models.TextField(_('descrição'), blank=True, max_length=3000)
	img = models.ImageField(_('imagem'), upload_to = inscricao_filepath, blank=True, validators=[validate_size])
	arquivo = models.FileField(_('arquivo'), upload_to = inscricao_filepath, blank=True, validators=[validate_size])
	def __str__(self):
		return self.nome
	def palafita_verbose(self):
		return dict(Projeto.palafitas)[self.palafita]

class Criterios(models.Model):
	texto = models.CharField('pt', max_length=300)
	texto_en = models.CharField('en', max_length=300, blank=True)
	def __str__(self):
		return self.texto
	class Meta:
		ordering = ['pk']

class AvaliacaoJuri(models.Model):
	inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
	juri = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	s2 = models.BooleanField('♥', default=False)
	texto = models.TextField(_('comentário'), blank=True, default='')
	media = models.FloatField(default=0)
	def __str__(self):
		return '%s_%s' % (self.juri, self.inscricao.codigo)

class Avaliacao(models.Model):
	notas=[]
	for i in range(11):
		notas.append((str(i),str(i)),)
	juri = models.ForeignKey(AvaliacaoJuri, on_delete=models.CASCADE)
	criterio = models.ForeignKey(Criterios, on_delete=models.CASCADE)
	nota = models.CharField('nota', choices=notas, max_length=2, default='0')
	def __str__(self):
		return '%s_%s' % (self.criterio.pk, self.nota)



