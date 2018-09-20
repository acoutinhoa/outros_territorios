from django import forms
from .models import *

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text', 'img')

class ResumoForm(forms.ModelForm):
	titulo = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Resumo
		fields = ('titulo', 'datas', 'resumo', 'imgs')
	def __init__ (self, *args, **kwargs):
		super(ResumoForm, self).__init__(*args, **kwargs)
		self.fields['imgs'].widget = forms.widgets.CheckboxSelectMultiple()
		self.fields['imgs'].queryset = Imagem.objects.all()
		# self.fields["preferences"].widget = forms.widgets.CheckboxSelectMultiple()
		# self.fields["preferences"].help_text = ""
		# self.fields["preferences"].queryset = FoodPreference.objects.filter(franchise=brand)
