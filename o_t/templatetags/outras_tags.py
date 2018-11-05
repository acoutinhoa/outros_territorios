from django import template
from django.template.defaultfilters import stringfilter, linebreaksbr
from django.urls import resolve, translate_url
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import random
import os

register = template.Library()

@register.filter(needs_autoescape=True)
def formatadata(text, car='', autoescape=True):
	text = text.split('\n')
	for i, par in enumerate(text):
		if ':' in par:
			par = par.split(':')
			text[i] = '%s%s<br><b>%s</b>' % (par[0], car, par[1])
	return mark_safe('<br><br>'.join(text))

@register.filter(needs_autoescape=True)
def post(text, imgs={}, autoescape=True):
	if text:
		text = text.split('[[')
		for i, par in enumerate(text[1:]):
			par = par.split(']]')
			tipo, info = par[0].split('=')
			tipo = tira_espacos(tipo)
			info = tira_espacos(info)
			if tipo == 'b':
				info = '<b>%s</b>' % (info)
			elif tipo == 'img':
				info = info.lower()
				if info in imgs:
					info = '<img src="%s" alt="%s" class="img_post">' % (imgs[info], info)
				else:
					info = ''
			else:
				info = '<a href="%s" target="_blank">%s</a>' % (info, tipo)
			text[i+1] = info + par[-1]
		return mark_safe(''.join(text).replace('\n','<br>'))
	return ''

def tira_espacos(info):
	if info[0] == ' ':
		info = info[1:]
	if info[-1] == ' ':
		info = info[:-1]
	return info

@register.filter
def filename(value, ext=True):
	filename = os.path.basename(value.file.name)
	filename = filename.replace('_', ' ')
	if not ext:
		filename = filename.split('.')[0]
	return filename

@register.simple_tag
def randint(min, max):
	return str(random.randint(min, max))

@register.simple_tag
def cem(n):
	return str(100-int(n))

@register.simple_tag
def cor(cor='acp', nao=''):
	cor_lista=[]
	for car in cor:
		if car == 'a':
			cor_lista.append('azul')
		elif car == 'c':
			cor_lista.append('cinza')
		elif car == 'p':
			cor_lista.append('preto')
	if nao in cor_lista:
		cor_lista.remove(nao)
	return random.choice(cor_lista)

@register.simple_tag
def espaco(min=40, max=100, u='px', autoescape=True, borda='linha'):
	return mark_safe('<div class="cartaz %s" style="height: %s%s;"></div>' % (borda, random.randint(min,max), u))

@register.simple_tag
def query(qs, tp, get=False, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    if tp == 'filter':
	    qs = qs.filter(**kwargs)
    elif tp == 'exclude':
	    qs = qs.exclude(**kwargs)
    if get:
    	qs = qs.first()
    return qs

@register.simple_tag
def set(val):
	return val

@register.simple_tag
def imgs_post(nota):
	imgs = {}
	if nota.imagem_set.all().exists():
		imagens = nota.imagem_set.all()
		for img in imagens:
			imgs[img.nome.lower()] = img.arquivo.url
	return imgs

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
	path = context['request'].path
	return translate_url(path,lang)

