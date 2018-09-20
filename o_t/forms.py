from django import forms
from .models import *

class NotaForm(forms.ModelForm):
	class Meta:
		model = Nota
		fields = ('titulo', 'texto', 'imagem')

class CartazForm(forms.ModelForm):
	titulo = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = Cartaz
		fields = ('titulo', 'datas', 'texto', 'imagens')
	def __init__ (self, *args, **kwargs):
		super(CartazForm, self).__init__(*args, **kwargs)
		self.fields['imagens'].widget = forms.widgets.CheckboxSelectMultiple()
		self.fields['imagens'].queryset = Imagem.objects.all()
