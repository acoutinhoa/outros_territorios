from django import template, get_version
from django.template.defaultfilters import stringfilter, linebreaksbr, floatformat
from django.urls import resolve, translate_url, reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from o_t.models import AvaliacaoJuri, Data
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

@register.filter
def grupo(user, group_name):
    return user.groups.filter(name=group_name).exists() 

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
def espaco(min=40, max=100, u='px', autoescape=True, borda='linha', tipo=''):
	if tipo:
		if tipo == 'random':
			tipos = ['dotted', 'dashed', 'double', ]
		else:
			tipos = [tipo]
		tipo = ''
		for b in borda.split(' '):
			if b == 'linha':
				tipo += 'border-bottom-style: %s;' % random.choice(tipos)
			elif b == 'linha_':
				tipo += 'border-top-style: %s;' % random.choice(tipos)
			elif b == 'coluna':
				tipo += 'border-right-style: %s;' % random.choice(tipos)
			elif b == 'coluna_':
				tipo += 'border-left-style: %s;' % random.choice(tipos)
	return mark_safe('<div class="cartaz %s" style="height: %s%s; %s"></div>' % (borda, random.randint(min,max), u, tipo))

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
				for n,c in enumerate(par[0]):
					if c == '=':
						break

				# tipo, info = par[0].split('=')
				tipo = tira_espacos(par[0][:n])
				info = tira_espacos(par[0][n+1:])
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
def hifen(peso=None):
	hifen = '-' * random.randint(2,19)
	if peso:
		return mark_safe('<span style="font-weight: %s;">%s</span>' % (peso, hifen))
	else:
		return hifen

@register.simple_tag
def borda():
	borda = ['dotted', 'dashed', 'double', ] #'groove',
	return mark_safe('style="border-top-style: dashed;"')
	# return mark_safe('style="border-top-style: %s;"' % random.choice(borda))

# @register.simple_tag
# def media(projeto):
# 	media = 0
# 	notas = Avaliacao.objects.filter(inscricao=projeto.inscricao)
# 	n = notas.count()
# 	for nota in notas:
# 		nota = int(nota.nota)
# 		if nota != 0:
# 			media += nota
# 		else:
# 			n -= 1
# 	if n != 0:
# 		media = media / n
# 	return str(floatformat(media))

@register.filter
def projeto(inscricao):
	return inscricao.projeto_set.all()[0]

@register.filter
def proximo(inscricoes, inscricao):
	for i, j in enumerate(inscricoes):
		if j == inscricao:
			break
	return inscricoes[i+1:]

@register.simple_tag
def ordem(ordem, user):
	tipos = ['data', 'nota', 'media', _('classificacao'), _('palafita'), _('pais'),]
	if ordem in tipos:
		tipos.remove(ordem)
	# if not ativo and grupo(user, 'juri'):
	# 	tipos.remove('media')
	# 	tipos.remove('palafita')
	if not user.is_authenticated:
		tipos.remove('nota')
		tipos.remove('data')
		tipos.remove('media')
	elif not grupo(user, 'juri'):
		tipos.remove('nota')
	return tipos

@register.filter
def acento(ordem):
	if ordem == 'classificacao':
		return 'classificação'
	if ordem == 'pais':
		return 'país'
	else:
		return ordem

@register.simple_tag
def galeria_feed(ordem, inscricoes, inscricao):
	feed = None
	txt = '''
			<div class="cartaz linha">
				<p class="titulo normal">%s</p>
			</div>'''

	if ordem == 'media' or ordem == _('classificacao'):
		for item in inscricoes:
			if item.selecao != feed:
				feed = item.selecao
				if item == inscricao:
					if item.selecao == 'ok':
						t = _('projetos selecionados')
					elif item.selecao == 'mh':
						t = _('menções honrosas')
					elif item.selecao == '':
						t = _('demais projetos')
					return mark_safe(txt % (t))
	
	elif ordem == _('palafita'):
		for item in inscricoes:
			if item.projeto_set.first().palafita != feed:
				feed = item.projeto_set.first().palafita
				if item == inscricao:
					return mark_safe(txt % ( formatapalafita(item.projeto_set.first().palafita_verbose()) ))

	elif ordem == _('pais'):
		for item in inscricoes:
			if item.dados_set.first().pais != feed:
				feed = item.dados_set.first().pais
				if item == inscricao:
					return mark_safe(txt % ( item.dados_set.first().select_verbose() ))

	elif ordem == _('data'):
		for item in inscricoes:
			if item.ok == 'no' and item.ok != feed:
				feed = item.ok
				if item == inscricao:
					return mark_safe(txt % ( 'reprovados' ))

	return ''

@register.filter
def info(inscricao, request):
	lista = [ 
	('Nome', inscricao.nome.title() + ' ' + inscricao.sobrenome.title() ), 
		('E-mail', inscricao.email ), 
		('Área', inscricao.select_verbose() ),
		('', ''),
	]
	for i, pessoa in enumerate(inscricao.equipe_set.all()):
		lista.append( ('equipe_%s' % (str(i+1)), '%s %s' % (pessoa.nome, pessoa.sobrenome)) )
		lista.append( ('e-mail', pessoa.email) )
		if i == inscricao.equipe_set.all().count()-1:
			lista.append( ('', '') )

	for i in inscricao.dados_set.values():
		for j in i:
			if j != 'id':
				if j == 'pais':
					lista.append( (j, inscricao.dados_set.first().select_verbose() ) )
				elif j == 'inscricao_id':
					link = request.build_absolute_uri(reverse('inscricoes', kwargs={'pk': inscricao.pk}))
					lista.append( ('código', inscricao.codigo) )
					lista.append( ('link', mark_safe('<a href="%s" target=_blank>%s</a>' % ( link, i[j]) )) )
				else:
					lista.append( (j, i[j]) )
				if j in ['inscricao_id', 'celular']:
					lista.append( ('', '') )
	return lista

# @register.simple_tag
# def media(qs, criterio=None):
# def media(qs, criterio=None):
# 	media = 0
# 	n = qs.count()
# 	for nota in qs:
# 		if criterio:
# 			if nota.avaliacao_set.filter(criterio=criterio).exists():
# 				nota = int(nota.avaliacao_set.get(criterio=criterio).nota)
# 			else:
# 				nota = 0
# 		else:
# 			nota = nota.media
# 		if nota == 0:
# 			n -= 1
# 		else:
# 			media += nota
# 	if n != 0:
# 		media = media / n
# 	return str(floatformat(media))

# @register.simple_tag
# def django():
# 	return 'django %s' % (get_version())
