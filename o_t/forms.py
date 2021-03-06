from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import *

NotaForm = forms.modelform_factory(
	Nota,
	fields = ('titulo', 'texto', 'titulo_en', 'texto_en', 'data1', 'tags',),
	widgets = {
		'titulo': forms.Textarea(attrs={'rows': 2}),
		'titulo_en': forms.Textarea(attrs={'rows': 2}),
		'texto': forms.Textarea(attrs={'rows': 25}),
		'texto_en': forms.Textarea(attrs={'rows': 25}),
		'tags' : forms.CheckboxSelectMultiple(attrs={'class': 'tags'}),
		},
	help_texts = {
		'data1' : 'formato: dd/mm/aaaa hh:mm:ss',	
	}, 
	)

ImagemForm = forms.inlineformset_factory(
	Nota, 
	Imagem, 
	extra=1,
	fields=('nome', 'arquivo',), 
	)

CartazForm = forms.modelform_factory(
	Cartaz,
	fields = ('titulo', 'datas', 'texto', 'titulo_en', 'datas_en', 'texto_en', ),
	widgets = {
		'titulo': forms.Textarea(attrs={'rows': 2}),
		'titulo_en': forms.Textarea(attrs={'rows': 2}),
		'texto': forms.Textarea(attrs={'rows': 20}),
		'texto_en': forms.Textarea(attrs={'rows': 20}),
		},
	help_texts = {
		# 'datas' : 'evento: data do evento\nevento2: data do evento2\n...',	
	}, 
	)

TagForm = forms.modelformset_factory(
	Tag,
	fields = ('tag', 'tag_en'),
	extra=1, 
	can_delete=True,
	)

ArquivoForm = forms.inlineformset_factory(
	Cartaz, 
	Arquivo, 
	extra=1,
	fields=('nome' ,'arquivo','en',), 
	)

ArquivoHomeForm = forms.inlineformset_factory(
	Cartaz, 
	Arquivo, 
	extra=1,
	fields=('imagem',), 
	)

LogosForm = forms.inlineformset_factory(
	Cartaz, 
	Arquivo, 
	extra=1,
	fields=('tipo', 'imagem', 'nome', 'altura','link' ), 
	)

JuriForm = forms.modelformset_factory(
	Juri, 
	fields=('nome', 'site', 'bio', 'bio_en'), 
	extra=1, 
	can_delete=True,
	)

# faq
FaqForm = forms.modelformset_factory(
	Faq, 
	fields=('pergunta', 'resposta', 'pergunta_en', 'resposta_en', 'publicar'), 
	extra=1, 
	can_delete=True,
	widgets = {
		'pergunta': forms.Textarea(attrs={'rows': 2}),
		'resposta': forms.Textarea(attrs={'rows': 5}),
		'pergunta_en': forms.Textarea(attrs={'rows': 2}),
		'resposta_en': forms.Textarea(attrs={'rows': 5}),
		},
	)

PerguntaForm = forms.modelform_factory(
	Pergunta,
	fields=('nome', 'email', 'consulta'),
	)

ConsultasForm = forms.modelformset_factory(
	Pergunta,
	extra=0, 
	fields=('bloco',),
	can_delete=True,
	)

RespostasForm = forms.modelformset_factory(
	Pergunta, 
	extra=0,
	fields=('bloco', 'pergunta', 'resposta', 'pergunta_en', 'resposta_en',), 
	widgets = {
		'pergunta': forms.Textarea(attrs={'rows': 2}),
		'resposta': forms.Textarea(attrs={'rows': 6}),
		'pergunta_en': forms.Textarea(attrs={'rows': 2}),
		'resposta_en': forms.Textarea(attrs={'rows': 6}),
		},
	can_delete=False,
	)

BlocoRespostasForm = forms.modelform_factory(
	BlocoRespostas,
	fields=('nome','nome_en'),
	)

# incricoes
InscricaoForm = forms.modelform_factory(
	Inscricao,
	fields=('email', 'nome', 'sobrenome', 'area'),
# 	labels={'termos':'''By ticking this box and submitting this Request Form I agree to treat all supplied information in the strictest confidence, and to not disclose the content to persons outside of my organisation / immediate bid team who will similarly treat such information in strict confidence.
# Your data is being collected and will be used for the purpose of potential participation in this competition only. Your data will not be used for any other purpose and will be deleted from all databases once the competition has come to a close and the winner is announced. If you wish to be removed from the database before this end point please email contato@outrosterritorios.com'''},
	)

# reenviar email
def validar_email(value):
	if not Inscricao.objects.filter(email=value).exists():
		raise ValidationError(_('Email não cadastrado'))

class EmailForm(forms.Form):
	email = forms.EmailField(label='E-mail', validators=[validar_email])

DadosForm = forms.modelform_factory(
	Dados, 
	# fields=None, 
	exclude = ('inscricao',), 
	widgets = {
	'nascimento': forms.SelectDateWidget(
		years = range(1900, 2001),
		)
	}, 
	labels = None, 
	help_texts = None, 
	error_messages = None, 
	)

EquipeForm = forms.inlineformset_factory(
	Inscricao, 
	Equipe, 
	extra=1,
	fields=('nome', 'sobrenome', 'email'), 
	)

ProjetoForm = forms.modelform_factory(
	Projeto,
	exclude = ('inscricao','slug'), 
	widgets = {
		'texto': forms.Textarea(attrs={'rows': 30}),
		'nome': forms.Textarea(attrs={'rows': 2}),
		},
	help_texts = {
		'img' : _('Tamanho máximo: 10MB') + ' %s JPG' % ('-' * random.randint(2,19)),	
		'arquivo' : _('Tamanho máximo: 10MB') + ' %s PDF' % ('-' * random.randint(2,19)),	
		}, 
	)

SelecaoForm = forms.modelform_factory(
	Inscricao,
	fields=('ok',),
	widgets = {
		'ok': forms.RadioSelect(attrs={'class': 'tags',}),
		},
	)

AvaliacaoForm = forms.modelform_factory(
	AvaliacaoJuri, 
	fields=('s2', 'texto', 'nota'), 
	widgets = {
		'texto': forms.Textarea(attrs={'rows': 3}),
		'nota': forms.RadioSelect(attrs={'class': 'tags', }),
		},
	)

SelecaoJuriForm = forms.modelform_factory(
	Inscricao,
	fields=('selecao',),
	widgets = {
		'selecao': forms.RadioSelect(attrs={'class': 'tags',}),
		},
	)

OrdemForm = forms.modelform_factory(
	Ordem,
	fields=('ordem',),
	widgets = {
		# 'ordem': forms.Select(choices=ordem_lista(Ordem.objects.all().count()),)
		},
	)

TextoJuriForm = forms.modelform_factory(
	Inscricao,
	fields=('texto','texto_en',),
	widgets = {
		'texto': forms.Textarea(attrs={'rows': 9}),
		'texto_en': forms.Textarea(attrs={'rows': 9}),
		},
	)

AtaForm = forms.modelform_factory(
	Ata,
	fields=('ata', 'ata_en', ),
	widgets = {
		},
	)

# from input_mask.widgets import InputMask

# class MyCustomInput(InputMask):
#    mask = {'cpf': '000.000.000-00'}
