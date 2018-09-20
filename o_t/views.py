from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from .forms import *
from .models import *
from random import *

def home(request, edit=False):
	titulo = 'home'
	frames = [
		[20, 'menu'],
		[50, 'c0'],
		[30, 'c1'],
	]
	# cartaz
	cartaz = get_object_or_404(Cartaz, pk=1)
	img = cartaz.imagens.all().order_by('?')[0]
	# blog
	notas = Nota.objects.filter(data1__lte=timezone.now()).order_by('-data1')
	# cartaz_edit
	form = None
	if edit:
		if request.method == 'POST':
			form = CartazForm(request.POST, instance=cartaz)
			if form.is_valid():
				cartaz = form.save()
				return redirect('home')
		else:
			form = CartazForm(instance=cartaz)

	return render(request, 'o_t/home.html', {
		'titulo': titulo, 
		'menu': def_menu(), 
		'frames': def_randomiza(frames),
		'borda': def_borda(),
		'cartaz': cartaz,
		'img': img,
		'notas': notas,
		'form': form,
		})

def concurso(request):
	titulo = 'concurso'
	frames = [
		[20, 'menu'],
		[50, 'c0'],
		[30, 'c1'],
	]
	return render(request, 'o_t/concurso.html', {
		'titulo': titulo, 
		'menu': def_menu(), 
		'frames': def_randomiza(frames),
		'borda': def_borda(),
		})

def galeria(request):
	titulo = 'galeria'
	frames = [
		[20, 'menu'],
		[50, 'c0'],
		[30, 'c1'],
	]
	return render(request, 'o_t/galeria.html', {
		'titulo': titulo, 
		'menu': def_menu(), 
		'frames': def_randomiza(frames),
		'borda': def_borda(),
		})

def blog(request, pk=None, edit=False):
	titulo = 'blog'
	frames = [
		[20, 'menu'],
		[50, 'c0'],
		[30, 'c1'],
	]
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
		'frames': def_randomiza(frames),
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
	frames = [
		[20, 'menu'],
		[50, 'c0'],
		[30, 'c1'],
	]
	return render(request, 'o_t/faq.html', {
		'titulo': titulo, 
		'menu': def_menu(), 
		'frames': def_randomiza(frames),
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

