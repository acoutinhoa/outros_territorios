from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django.forms import modelform_factory, modelformset_factory, inlineformset_factory
from random import randint, randrange
from .forms import *
from .models import *

frames = [
	[20, 'menu'],
	[50, 'c0'],
	[30, 'c1'],
]

def home(request, edit=False, pk=1):
	titulo = 'home'
	# cartaz
	cartaz = get_object_or_404(Cartaz, pk=pk)
	img = cartaz.arquivo_set.all().order_by('?')[0]
	# blog
	notas = Nota.objects.filter(data1__lte=timezone.now()).order_by('-data1')
	# cartaz_edit
	form = None
	formset = None
	if edit:
		ArquivoFormSet = inlineformset_factory(Cartaz, Arquivo, fields=('nome', 'arquivo'))
		if request.method == 'POST':
			form = CartazForm(request.POST, request.FILES, instance=cartaz)
			formset = ArquivoFormSet(request.POST, request.FILES, instance=cartaz)
			if formset.is_valid() and form.is_valid():
				cartaz = form.save()
				formset.save()
				return redirect('home')
		else:
			form = CartazForm(instance=cartaz)
			formset = ArquivoFormSet(instance=cartaz)

	return render(request, 'o_t/home.html', {
		'titulo': titulo, 
		'menu': def_menu(), 
		'frames': frames,
		'borda': def_borda(),
		'cartaz': cartaz,
		'img': img,
		'notas': notas,
		'form': form,
		'formset': formset,
		})

def concurso(request, edit=False, pk=2):
	titulo = 'concurso'
	# cartaz
	cartaz = get_object_or_404(Cartaz, pk=pk)
	arquivos = cartaz.arquivo_set.all()
	# juri
	jurados = Juri.objects.all()
	# cartaz_edit
	form = None
	formset = None
	formset_ = None
	if edit:
		ArquivoFormSet = inlineformset_factory(Cartaz, Arquivo, fields=('nome', 'arquivo'), )
		JuriFormSet = modelformset_factory(Juri, fields=('nome', 'site', 'bio'), extra=2, can_delete=True)
		if request.method == 'POST':
			form = CartazForm(request.POST, instance=cartaz)
			formset = ArquivoFormSet(request.POST, request.FILES, instance=cartaz)
			formset_ = JuriFormSet(request.POST)
			if formset.is_valid() and formset_.is_valid() and form.is_valid():
				cartaz = form.save()
				formset.save()
				formset_.save()
				return redirect('concurso')
		else:
			form = CartazForm(instance=cartaz)
			formset = ArquivoFormSet(instance=cartaz)
			formset_ = JuriFormSet()

	return render(request, 'o_t/concurso.html', {
		'titulo': titulo, 
		'menu': def_menu(), 
		'frames': frames,
		'borda': def_borda(),
		'cartaz': cartaz,
		'arquivos': arquivos,
		'form': form,
		'formset': formset,
		'formset_': formset_,
		'jurados': jurados,
		})

def galeria(request):
	titulo = 'galeria'
	return render(request, 'o_t/galeria.html', {
		'titulo': titulo, 
		'menu': def_menu(), 
		'frames': frames,
		'borda': def_borda(),
		})

def blog(request, pk=None, edit=False):
	titulo = 'blog'
	notas = Nota.objects.filter(data1__lte=timezone.now()).order_by('-data1')
	notas_ = Nota.objects.exclude(data1__lte=timezone.now()).order_by('-data0')
	nota = None
	form = None
	if pk:
		nota = get_object_or_404(Nota, pk=pk)
	if edit:
		if request.method == 'POST':
			form = NotaForm(request.POST, request.FILES, instance=nota)
			if form.is_valid():
				nota = form.save(commit=False)
				nota.autor = request.user
				nota.save()
				return redirect('blog', pk=nota.pk)
		else:
			form = NotaForm(instance=nota)

	return render(request, 'o_t/blog.html', {
		'titulo': titulo, 
		'menu': def_menu(), 
		'frames': frames,
		'borda': def_borda(),
		'notas': notas,
		'notas_': notas_,
		'nota': nota,
		'form': form,
		})

@login_required
def nota_publish(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    nota.publish()
    return redirect('blog', pk=pk)

@login_required
def nota_remove(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    nota.delete()
    return redirect('blog')


def faq(request):
	titulo = 'faq'
	return render(request, 'o_t/faq.html', {
		'titulo': titulo, 
		'menu': def_menu(), 
		'frames': frames,
		'borda': def_borda(),
		})


################### funcoes

def def_menu():
	menu = [
		['home', []],
		['concurso', ["documentação",'juri','inscrições',]],
		['galeria', []],
		['blog', []],
		['faq', []],
	]
	for n, i in enumerate(menu):
		url = reverse(i[0])
		menu[n].insert(1, url)
	return menu

def def_randomiza(lista):
	l = []
	for i in range(len(lista)):
		l.append(lista.pop(randrange(len(lista))))
	return l

def def_borda(x=5, y=25):
	return str(randint(x, y)) + 'px'

