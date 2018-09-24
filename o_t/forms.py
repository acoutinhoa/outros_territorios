from django import forms
from .models import *

class NotaForm(forms.ModelForm):
	class Meta:
		model = Nota
		fields = ('titulo', 'texto', 'imagem')

class CartazForm(forms.ModelForm):
	class Meta:
		model = Cartaz
		fields = ('titulo', 'datas', 'texto')
