from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from .forms import PostForm
from .models import *
from random import *

def home(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('?')
	pk = posts[0].pk
	frames = def_randomiza([
		[100, 20, reverse('menu')],
		[100, 50, reverse('resumo', args=('1',))],
		[100, 30, reverse('post_list')],
	])
	borda = def_borda()
	return render(request, 'blog/iframe.html', {'frames': frames, 'tipo': 'coluna', 'borda': borda,})


def menu(request):
	itens_menu = [
		('concurso', ["documentação",'juri','inscrições',]),
		('galeria', []),
		('blog', []),
		('faq', []),
	]
	borda = def_borda()
	return render(request, 'blog/menu.html', {'itens_menu': itens_menu, 'borda': borda,})

def resumo(request, pk):
	resumo = get_object_or_404(Resumo, pk=pk)
	img = resumo.imgs.all().order_by('?')[0]
	borda = def_borda()
	return render(request, 'blog/resumo.html', {'resumo':resumo, 'img':img, 'borda': borda,})

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('?')
	borda = def_borda()
	return render(request, 'blog/post_list.html', {'posts': posts, 'borda': borda,})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	borda = def_borda()
	return render(request, 'blog/post_detail.html', {'post': post, 'borda': borda,})

def post_new(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	borda = def_borda()
	return render(request, 'blog/post_edit.html', {'form': form, 'borda': borda,})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	borda = def_borda()
	return render(request, 'blog/post_edit.html', {'form': form, 'borda': borda,})


# defs

def def_randomiza(lista):
	l = []
	for i in range(len(lista)):
		l.append(lista.pop(randrange(len(lista))))
	return l

def def_borda(x=5, y=25):
	return str(randint(x, y)) + 'px'
