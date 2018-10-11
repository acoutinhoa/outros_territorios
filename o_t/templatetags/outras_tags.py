from django import template
from django.template.defaultfilters import stringfilter, linebreaksbr
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import random
import os

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def paragrafo(text, autoescape=True):
	text=text.split('\n')
	t = ''
	for par in text:
		t += par + 2*'\n'
	return mark_safe(linebreaksbr(t[:-2]))

@register.filter(needs_autoescape=True)
def formatadata(text, car='', autoescape=True):
	text=text.split('\n')
	t = ''
	for par in text:
		if ':' in par:
			par=par.split(':')
			t += '%s%s<br><b>%s</b><br><br>' % (par[0], car, par[1])
		else:
			t += par + '<br><br>'
	return mark_safe(t[:-8])

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



# @register.filter(name='cut')
# def cut(value, arg):
#     return value.replace(arg, '')

# @register.filter
# @stringfilter
# def lower(value):
#     return value.lower()



# from django import template
# from django.utils.html import conditional_escape
# from django.utils.safestring import mark_safe

# register = template.Library()

# @register.filter(needs_autoescape=True)
# def initial_letter_filter(text, autoescape=True):
#     first, other = text[0], text[1:]
#     if autoescape:
#         esc = conditional_escape
#     else:
#         esc = lambda x: x
#     result = '<strong>%s</strong>%s' % (esc(first), esc(other))
#     return mark_safe(result)