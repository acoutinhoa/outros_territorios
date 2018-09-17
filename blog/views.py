from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from .forms import PostForm
from .models import *
import random

def home(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('?')
	pk = posts[0].pk
	frames = def_randomiza([
		[100, 20, reverse('menu')],
		# [100, 45, reverse('post_detail', args=(str(pk)))],
		[100, 50, reverse('resumo', args=('1'))],
		[100, 30, reverse('post_list')],
	])
	return render(request, 'blog/iframe.html', {'frames': frames, 'tipo': 'coluna'})


def menu(request):
	itens_menu = [
		('concurso', ["documentação",'juri','inscrições',]),
		('galeria', []),
		('blog', []),
		('faq', []),
	]
	logo = []
	for i in range(random.randint(3,10)):
		logo.append('logo')
	return render(request, 'blog/menu.html', {'itens_menu': itens_menu, 'logo': logo})

def resumo(request, pk):
	resumo = get_object_or_404(Resumo, pk=pk)
	img = resumo.imgs.all().order_by('?')[0]
	return render(request, 'blog/resumo.html', {'resumo':resumo, 'img':img})

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('?')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

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
	return render(request, 'blog/post_edit.html', {'form': form})

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
	return render(request, 'blog/post_edit.html', {'form': form})


# defs

def def_randomiza(lista):
	l = []
	for i in range(len(lista)):
		l.append(lista.pop(random.randrange(len(lista))))
	return l

