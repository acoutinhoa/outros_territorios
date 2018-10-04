from django import template
from django.template.defaultfilters import stringfilter, linebreaksbr
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
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
		par=par.split(':')
		t += '%s%s<br><b>%s</b><br><br>' % (par[0], car, par[1])
	return mark_safe(t[:-8])

@register.filter
def filename(value):
	filename = os.path.basename(value.file.name)
	filename = filename.replace('_', ' ')
	return filename



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