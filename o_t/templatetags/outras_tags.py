from django import template, get_version
from django.template.defaultfilters import stringfilter, linebreaksbr
from django.urls import resolve, translate_url
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
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

@register.filter()
def formatapalafita(txt):
	return txt.split(' ')[-1]

@register.filter
def filename(value, ext=True):
	filename = os.path.basename(value.file.name)
	filename = filename.replace('_', ' ')
	if not ext:
		filename = filename.split('.')[0]
	return filename

@register.filter
def alien(txt):
	if 'aline coutinho' in txt or 'alien coutinho' in txt:
		txt = txt.split(' ')
		for i,p in enumerate(txt):
			if '\n' in p:
				p = p.split('\n')
				for j,pp in enumerate(p):
					if pp == 'aline' or pp == 'alien':
						p[j] = random.choice(['aline', 'alien'])
				txt[i] = '\n'.join(p)

			else:
				if p == 'aline' or p == 'alien':
					txt[i] = random.choice(['aline', 'alien'])
		txt = ' '.join(txt)
	return txt

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

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
	path = context['request'].path
	return translate_url(path,lang)


@register.filter(needs_autoescape=True)
def post(text, imgs={}, autoescape=True):
	if text:
		text = text.split('[[')
		for i, par in enumerate(text[1:]):
			par = par.split(']]')
			if '=' in par[0]:
				tipo, info = par[0].split('=')
				tipo = tira_espacos(tipo)
				info = tira_espacos(info)
				if tipo == 'b':
					info = '<b>%s</b>' % (info)
				elif tipo == 'img':
					info = info.lower()
					gs = ''
					if '|' in info:
						info, gs = info.split('|')
					if info in imgs:
						if gs:
							gs = 'style="-webkit-filter: grayscale({0}%); filter: grayscale({0}%);"'.format(gs)
						info = '<img src="%s" alt="%s" class="img_post" %s>' % (imgs[info], info, gs)
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

@register.simple_tag
def imgs_post(nota):
	imgs = {}
	if nota.imagem_set.all().exists():
		imagens = nota.imagem_set.all()
		for img in imagens:
			imgs[img.nome.lower()] = img.arquivo.url
	return imgs


@register.simple_tag
def post_format(nota, txt, link, crop=False):
	imgs = imgs_post(nota)

	botao = False
	lista = ['[[ + ]]', '[[+]]', '[[ +]]', '[[+ ]]']
	for mais in lista:
		if mais in txt:
			if crop:
				txt = txt.split(mais)[0]
				botao = True
			else:
				txt = txt.replace(mais,'')

	txt = post(txt, imgs)
	if botao:
		txt += '<a href="%s">%s</a>' % (link, _('ver mais'))

	return mark_safe(txt)

@register.simple_tag
def hifen():
	return '-' * random.randint(2,19)

# @register.simple_tag
# def django():
# 	return 'django %s' % (get_version())
