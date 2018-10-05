from django.core.exceptions import ValidationError
from django import forms
from .models import *

class NotaForm(forms.ModelForm):
	class Meta:
		model = Nota
		fields = ('titulo', 'texto', 'imagem')

CartazForm = forms.modelform_factory(
	Cartaz,
	fields = ('titulo', 'datas', 'texto'),
	widgets = {
		'titulo': forms.Textarea(attrs={'rows': 2}),
		},
	)

ArquivoFormSet = forms.inlineformset_factory(
	Cartaz, 
	Arquivo, 
	extra=1,
	fields=('arquivo',), 
	)

LogosFormSet = forms.inlineformset_factory(
	Cartaz, 
	Arquivo, 
	extra=1,
	fields=('tipo', 'arquivo',), 
	)

JuriFormSet = forms.modelformset_factory(
	Juri, 
	fields=('nome', 'site', 'bio'), 
	extra=1, 
	can_delete=True,
	)

# faq
FaqFormSet = forms.modelformset_factory(
	Faq, 
	fields=('pergunta', 'resposta', 'publicar'), 
	extra=1, 
	can_delete=True,
	widgets = {
		'pergunta': forms.Textarea(attrs={'rows': 2}),
		'resposta': forms.Textarea(attrs={'rows': 5}),
		},
	)

PerguntaForm = forms.modelform_factory(
	Pergunta,
	fields=('nome', 'email', 'consulta'),
	)

ConsultasFormSet = forms.modelformset_factory(
	Pergunta,
	extra=0, 
	fields=('bloco',),
	can_delete=True,
	)

RespostasFormSet = forms.modelformset_factory(
	Pergunta, 
	extra=0,
	fields=('bloco', 'pergunta', 'resposta',), 
	widgets = {
		'pergunta': forms.Textarea(attrs={'rows': 2}),
		'resposta': forms.Textarea(attrs={'rows': 6}),
		},
	can_delete=False,
	)

BlocoRespostasForm = forms.modelform_factory(
	BlocoRespostas,
	fields=('nome',),
	labels={'nome':'novo bloco'},
	)

# incricoes
InscricaoForm = forms.modelform_factory(
	Inscricao,
	fields=('nome', 'email', 'area', 'termos'),
	labels={'termos':'''
By ticking this box and submitting this Request Form I agree to treat all supplied information in the strictest confidence, and to not disclose the content to persons outside of my organisation / immediate bid team who will similarly treat such information in strict confidence.
Your data is being collected and will be used for the purpose of potential participation in this competition only. Your data will not be used for any other purpose and will be deleted from all databases once the competition has come to a close and the winner is announced. If you wish to be removed from the database before this end point please email contato@outrosterritorios.com'''},
	)

# reenviar email
def validar_email(value):
	if not Inscricao.objects.filter(email=value).exists():
		raise ValidationError('email nao cadastrado')

class EmailForm(forms.Form):
	email = forms.EmailField(label='E-mail', validators=[validar_email])

DadosForm = forms.modelform_factory(
	Dados, 
	# fields=None, 
	exclude = ('inscricao',), 
	widgets = {
	'nascimento': forms.SelectDateWidget(
		years = range(1900, 2001),
		months = {
		    1:('01'), 2:('02'), 3:('03'), 4:('04'),
		    5:('05'), 6:('06'), 7:('07'), 8:('08'),
		    9:('09'), 10:('10'), 11:('11'), 12:('12')
			},
		)
	}, 
	labels = None, 
	help_texts = None, 
	error_messages = None, 
	)

EquipeFormSet = forms.inlineformset_factory(
	Inscricao, 
	Equipe, 
	extra=1,
	fields=('nome', 'email'), 
	)

ProjetoForm = forms.inlineformset_factory(
	Inscricao, 
	Projeto,
	extra=1,
	max_num=1,
	validate_max=True,
	can_delete=False,
	fields=('nome', 'img', 'texto'),
	)

PranchaFormSet = forms.inlineformset_factory(
	Inscricao, 
	Prancha, 
	extra=3,
	max_num=3,
	validate_max=True,
	can_delete=False,
	fields=('img',),
	)


# from input_mask.widgets import InputMask

# class MyCustomInput(InputMask):
#    mask = {'cpf': '000.000.000-00'}
