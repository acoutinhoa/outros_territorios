from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.core.mail import BadHeaderError, send_mail, send_mass_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate, get_language
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F
from random import randint, randrange, choice
from .forms import *
from .models import *

menu = [
	[_('início'), reverse_lazy('home'), []],
	[_('chamada de projetos'), reverse_lazy('concurso'), [
		(_('inscrições'), _('inscricoes')),
		(_('ata de julgamento'), _('ata')),
		(_('arquivos adicionais'), _('arquivos')), 
		(_('cronograma'), _('cronograma')), 
		(_('júri'), _('juri')),
		]],
	[_('galeria'), reverse_lazy('galeria'), []],
	[_('blog'), reverse_lazy('blog'), []],
	[_('perguntas frequentes'), reverse_lazy('faq'), []],
	]

msg_inscricao = _('''Olá {nome},
Sua inscrição foi realizada com sucesso!
Seu código de identificação é {codigo}. Sua proposta deverá ser enviada através do link a seguir, que ficará disponível até a data limite definida no nosso cronograma. Cada link é único e deve ser utilizado para envio de um único projeto apenas.
Acompanhe as atualizações no nosso blog.
Dúvidas só serão respondidas através do nosso site.
_
Link para envio da proposta:
{link}''')

msg_email = _('''Olá {nome},
Segue novamente o link para envio da sua proposta.
_
Link para envio da proposta:
{link}''')

msg_consulta = _('''Olá {nome},
Recebemos sua consulta. Ela será respondida no site no próximo bloco de respostas.
_
Consulta:
{consulta}''')

msg_publicacao_consulta = _('''Olá {nome},
Sua consulta foi respondida.
_
Consulta:
{consulta}

Resposta:
{resposta}
_
Link para bloco de respostas:
{link}''')

# teste usuario nao é juri
def not_juri(user):
	if user.groups.filter(name='juri').exists():
		return False
	else:
		return True


def home(request):
	titulo = _('início')
	cartaz = Cartaz.objects.get_or_create(pagina='home')[0]
	notas = Nota.objects.filter(data1__lte=timezone.now())
	# logos
	logos = Cartaz.objects.get_or_create(pagina='logos')[0]
	logos = Arquivo.objects.filter(pagina=logos)
	# img
	img = None
	if cartaz.arquivo_set.all().exists():
		# img = cartaz.arquivo_set.all()
		img = cartaz.arquivo_set.all().order_by('?')[0]

	# paginacao
	page = request.GET.get('page', 1)
	paginator = Paginator(notas, 5)
	try:
		notas_pg = paginator.page(page)
	except PageNotAnInteger:
		notas_pg = paginator.page(1)
	except EmptyPage:
		notas_pg = paginator.page(paginator.num_pages)

	return render(request, 'o_t/home.html', {
		'edit': 'home_edit',
		'titulo': titulo, 
		'menu': menu, 
		'logos': logos,
		'cartaz': cartaz,
		'img': img,
		'notas_pg': notas_pg,
	})

@login_required
@user_passes_test(not_juri)
def home_edit(request):
	titulo = _('início')+'/edit'
	cartaz = Cartaz.objects.get_or_create(pagina='home')[0]
	logos = Cartaz.objects.get_or_create(pagina='logos')[0]

	if request.method == 'POST':
		if 'cartaz_submit' in request.POST or 'cartaz_submit_home' in request.POST:
			cartaz_form = CartazForm(request.POST, instance=cartaz)
			arquivos_form = ArquivoHomeForm(request.POST, request.FILES, instance=cartaz)
			if arquivos_form.is_valid() and cartaz_form.is_valid():
				cartaz_form.save()
				arquivos_form.save()
				arquivos_form = ArquivoHomeForm(instance=cartaz)
				if 'cartaz_submit_home' in request.POST:
					return redirect('home')
			logos_form = LogosForm(instance=logos)
		elif 'logos_submit' in request.POST or 'logos_submit_home' in request.POST:
			logos_form = LogosForm(request.POST, request.FILES, instance=logos)
			if logos_form.is_valid():
				logos_form.save()
				if 'logos_submit_home' in request.POST:
					return redirect('home')
				logos_form = LogosForm(instance=logos)
			cartaz_form = CartazForm(instance=cartaz)
			arquivos_form = ArquivoHomeForm(instance=cartaz)
	else:
		cartaz_form = CartazForm(instance=cartaz)
		arquivos_form = ArquivoHomeForm(instance=cartaz)
		logos_form = LogosForm(instance=logos)

	return render(request, 'o_t/home_edit.html', {
		'titulo': titulo, 
		'menu': menu, 
		'cartaz': cartaz,
		'cartaz_form': cartaz_form,
		'arquivos_form': arquivos_form,
		'logos_form': logos_form,
	})

def concurso(request, msg='',):
	titulo = _('chamada de projetos')
	cartaz = Cartaz.objects.get_or_create(pagina='concurso')[0]
	arquivos = None
	if cartaz.arquivo_set.all().exists():
		arquivos = cartaz.arquivo_set.all()
	jurados = Juri.objects.all()

	# ata
	ata = Ata.objects.get_or_create(pagina=cartaz)[0]

	msg = msg.replace('-', ' ')
	if 'Inscricao' in msg:
		msg = msg.replace('Inscricao', 'Inscrição')

	if request.method == 'POST':
		if 'inscricao_submit' in request.POST:
			inscricao_form = InscricaoForm(request.POST, prefix='inscricao')
			dados_form = DadosForm(request.POST, prefix='dados')
			if inscricao_form.is_valid() and dados_form.is_valid():
				inscricao = inscricao_form.save()
				dados = dados_form.save(commit=False)
				dados.inscricao = inscricao
				dados.save()
				# enviar email
				link = request.build_absolute_uri(reverse('inscricoes', kwargs={'pk': inscricao.pk}))
				assunto = _('Outros Territórios_confirmação de inscrição')
				msg = msg_inscricao.format(nome=inscricao.nome, codigo=inscricao.codigo, link=link)
				send_mail(assunto, msg, settings.EMAIL_HOST_USER, [inscricao.email,])
				return redirect('confirmacao', msg=_('Inscricao-realizada'))
				# return redirect('inscricoes', pk=inscricao.pk)
			email_form = EmailForm(prefix='email', label_suffix='')
		elif 'email_submit' in request.POST:
			email_form = EmailForm(request.POST, prefix='email')
			if email_form.is_valid():
				email = email_form.cleaned_data['email']
				inscricao = Inscricao.objects.get(email=email)
				# enviar email
				link = request.build_absolute_uri(reverse('inscricoes', kwargs={'pk': inscricao.pk}))
				assunto = _('Outros Territórios_reenvio de link')
				msg = msg_email.format(nome=inscricao.nome, link=link)
				send_mail(assunto, msg, settings.EMAIL_HOST_USER, [inscricao.email,])
				return redirect('confirmacao', msg=_('Email-enviado'))
			inscricao_form = InscricaoForm(prefix='inscricao', label_suffix='')
			dados_form = DadosForm(prefix='dados', label_suffix='')
	else:
		inscricao_form = InscricaoForm(prefix='inscricao', label_suffix='')
		dados_form = DadosForm(prefix='dados', label_suffix='')
		email_form = EmailForm(prefix='email', label_suffix='')

	return render(request, 'o_t/concurso.html', {
		'edit': 'concurso_edit',
		'titulo': titulo, 
		'menu': menu, 
		'cartaz': cartaz,
		'arquivos': arquivos,
		'jurados': jurados,
		'inscricao_form': inscricao_form,
		'dados_form': dados_form,
		'email_form': email_form,
		'confirmacao': msg,
		'ata': ata,
	})

@login_required
@user_passes_test(not_juri)
def concurso_edit(request):
	titulo = _('chamada de projetos')
	cartaz = Cartaz.objects.get_or_create(pagina='concurso')[0]
	ata = Ata.objects.get_or_create(pagina=cartaz)[0]

	if request.method == 'POST':
		if 'juri_submit' in request.POST or 'juri_submit_home' in request.POST:
			juri_form = JuriForm(request.POST, prefix='juri')
			ata_form = AtaForm(request.POST, request.FILES, instance=ata, prefix='ata')
			if juri_form.is_valid() and ata_form.is_valid():
				juri_form.save()
				ata_form.save()
				if 'juri_submit_home' in request.POST:
					return redirect('concurso')
				juri_form = JuriForm(prefix='juri')
				ata_form = AtaForm(instance=ata, prefix='ata')
			cartaz_form = CartazForm(instance=cartaz, prefix='cartaz')
			arquivos_form = ArquivoForm(instance=cartaz, prefix='arquivo')
		elif 'cartaz_submit' in request.POST or 'cartaz_submit_home' in request.POST:
			cartaz_form = CartazForm(request.POST, instance=cartaz, prefix='cartaz')
			arquivos_form = ArquivoForm(request.POST, request.FILES, instance=cartaz, prefix='arquivo')
			if arquivos_form.is_valid() and cartaz_form.is_valid():
				cartaz = cartaz_form.save()
				arquivos_form.save()
				if 'cartaz_submit_home' in request.POST:
					return redirect('concurso')
				arquivos_form = ArquivoForm(instance=cartaz, prefix='arquivo')
			juri_form = JuriForm(prefix='juri')
			ata_form = AtaForm(instance=ata, prefix='ata')
	else:
		cartaz_form = CartazForm(instance=cartaz, prefix='cartaz')
		arquivos_form = ArquivoForm(instance=cartaz, prefix='arquivo')
		ata_form = AtaForm(instance=ata, prefix='ata')
		juri_form = JuriForm(prefix='juri')

	return render(request, 'o_t/concurso_edit.html', {
		'titulo': titulo, 
		'menu': menu, 
		'cartaz_form': cartaz_form,
		'arquivos_form': arquivos_form,
		'ata_form': ata_form,
		'juri_form': juri_form,
	})


def email(request):
	titulo = _('email')
	inscritos = Inscricao.objects.filter(finalizada=None)
	finalizados = Inscricao.objects.exclude(finalizada=None)

	return render(request, 'o_t/email.html', {
		'titulo': titulo, 
		'menu': menu, 
		'inscritos': inscritos, 
		'finalizados': finalizados, 
		'noindex': True,
	})

def inscricoes(request, pk, erro=False,):
	titulo = _('inscrições')
	inscricao = get_object_or_404(Inscricao, pk=pk)
	dados = Dados.objects.get(inscricao=inscricao)
	projeto = Projeto.objects.get_or_create(inscricao=inscricao)[0]
	dados_form = DadosForm(instance=dados, prefix='dados')
	c0 = '27'
	c1 = '43'
	c2 = '30'

	ativo = False
	finaliza = Data.objects.all()[0].fim
	if timezone.now() < finaliza:
		ativo = True

	if erro:
		erro = _('Você precisa preencher todos os campos do projeto para finalizar sua inscrição')

	if request.method == 'POST':
		if 'equipe_submit' in request.POST:
			equipe_form = EquipeForm(request.POST, instance=inscricao, prefix='equipe')
			if equipe_form.is_valid():
				equipe_form.save()
				equipe_form = EquipeForm(instance=inscricao, prefix='equipe')
				return redirect('inscricoes', pk=pk)
			projeto_form = ProjetoForm(instance=projeto, prefix='projeto')
		elif 'projeto_submit' in request.POST:
			projeto_form = ProjetoForm(request.POST, request.FILES, instance=projeto, prefix='projeto')
			if projeto_form.is_valid():
				projeto_form.save()
				return redirect('inscricoes', pk=pk)
			equipe_form = EquipeForm(instance=inscricao, prefix='equipe')
	else:
		equipe_form = EquipeForm(instance=inscricao, prefix='equipe')
		projeto_form = ProjetoForm(instance=projeto, prefix='projeto')

	return render(request, 'o_t/inscricoes.html', {
		'titulo': titulo, 
		'inscricao': inscricao, 
		'dados_form': dados_form,
		'equipe_form': equipe_form,
		'projeto_form': projeto_form,
		'c0': c0,
		'c1': c1,
		'c2': c2,
		'erro': erro,	
		'ativo': ativo,	
		'noindex': True,
	})

def inscricoes_submit(request, pk,):
	inscricao = get_object_or_404(Inscricao, pk=pk)
	projeto = Projeto.objects.get(inscricao=inscricao)

	if projeto.palafita and projeto.nome and projeto.texto and projeto.img and projeto.arquivo:
		inscricao.finaliza()
		return redirect('inscricoes', pk=pk)
	else:
		return redirect('inscricoes_erro', pk=pk)

def galeria(request, codigo=None, ordem=''):
	titulo = _('galeria')
	cartaz = Cartaz.objects.get_or_create(pagina='galeria')[0]

	# ativo = 0
	# if Data.objects.filter(nome='juri').exists():
	# 	dt = Data.objects.get(nome='juri').fim
	# 	if timezone.now() > dt:
	# 		ativo = 1


	if not ordem:
		ordem = _('classificacao')

	if not_juri(request.user) and ordem == 'data':
		inscricoes = Inscricao.objects.exclude(finalizada=None)
	else:
		inscricoes = Inscricao.objects.filter(ok='ok')

	if ordem == 'data':
		inscricoes = inscricoes.order_by('-ok', 'finalizada',)
	elif ordem == 'media':
		inscricoes = inscricoes.order_by('-selecao', 'ordem__ordem', '-media', '-s2', 'finalizada')
	elif ordem == 'nota' and not not_juri(request.user):
		inscricoes = inscricoes.filter(avaliacaojuri__juri=request.user, avaliacaojuri__nota__gte='0').order_by('-avaliacaojuri__nota', '-s2', 'finalizada')

	elif ordem == _('palafita'):
		inscricoes = inscricoes.order_by('projeto__palafita', 'projeto__nome')
	elif ordem == _('classificacao'):
		inscricoes = inscricoes.order_by('-selecao', 'ordem__ordem', 'projeto__nome')
	elif ordem == _('pais'):
		inscricoes = inscricoes.order_by('dados__pais', 'projeto__nome')
	else:
		return redirect('galeria')


	form = None
	selecao_form = None
	ordem_form = None
	texto_form = None
	proximo = None
	
	if codigo:
		inscricao =  get_object_or_404(Inscricao, codigo=codigo)
		# calcula proximo
		for i, j in enumerate(inscricoes):
			if j == inscricao:
				break
		i += 1
		if i < len(inscricoes):
			proximo = inscricoes[i]

		if not not_juri(request.user):
			juri = AvaliacaoJuri.objects.get_or_create(inscricao=inscricao, juri=request.user)[0]

		if Ordem.objects.filter(inscricao=inscricao).exists():
			selecionado = Ordem.objects.get(inscricao=inscricao)
		else:
			selecionado = None

		if request.user.is_authenticated:
			if request.method == 'POST':
				if request.user.is_authenticated and not_juri(request.user):
					# pre selecao
					form = SelecaoForm(request.POST, instance=inscricao)
					if form.is_valid():
						form.save()
					# texto
					if inscricao.selecao:
						texto_form = TextoJuriForm(request.POST, prefix='texto', instance=inscricao, label_suffix='')
						if texto_form.is_valid():
							texto_form.save()
					# ordem
					if selecionado:
						ordem_data = Ordem.objects.filter(inscricao=inscricao).values()[0]
						ordem_form = OrdemForm(request.POST, instance=selecionado, label_suffix='', initial=ordem_data)
						if ordem_form.is_valid():
							if ordem_form.has_changed():
								novo = ordem_form.save(commit=False)
								lista = []
								for p in Ordem.objects.exclude(inscricao=inscricao):
									lista.append(p.inscricao)
								lista.insert(int(novo.ordem)-1, novo.inscricao)
								for i,p in enumerate(lista):
									p = Ordem.objects.get(inscricao=p)
									p.ordem = str(i+1)
									p.save()
					# selecao
					data = Inscricao.objects.filter(codigo=codigo).values('selecao')[0]
					selecao_form = SelecaoJuriForm(request.POST, instance=inscricao, label_suffix='', initial=data)
					if selecao_form.is_valid():
						selecao_form.save()
						if selecao_form.has_changed():
							if inscricao.selecao == 'ok':
								if not Ordem.objects.filter(inscricao=inscricao).exists():
									n = len(Ordem.objects.all())
									Ordem.objects.create(inscricao=inscricao, ordem=str(n+1))
							else:
								if selecionado:
									for p in Ordem.objects.filter(ordem__gt=selecionado.ordem):
										n = int(p.ordem)
										p.ordem = str(n-1)
										p.save()
									selecionado.delete()

				# # vazio
				# if not_juri(request.user):
				# 	form = SelecaoForm(request.POST, instance=inscricao)
				# 	if form.is_valid():
				# 		form.save()

				# 	texto_form = TextoJuriForm(request.POST, prefix='texto', instance=inscricao)
				# 	if texto_form.is_valid():
				# 		texto_form.save()
				# # juri
				# else:
				# 	data = AvaliacaoJuri.objects.filter(inscricao=inscricao, juri=request.user).values()[0]
				# 	form = AvaliacaoForm(request.POST, instance=juri, prefix='juri', label_suffix='', initial=data)
				# 	if form.is_valid():
				# 		form.save()
				# 		if form.has_changed():
				# 			# likes
				# 			if 's2' in form.changed_data:
				# 				inscricao.s2 = len(AvaliacaoJuri.objects.filter(inscricao=inscricao, s2=True))
				# 				inscricao.save()
				# 			# media
				# 			if 'nota' in form.changed_data:
				# 				media = 0
				# 				notas = AvaliacaoJuri.objects.filter(inscricao=inscricao)
				# 				n = len(notas)
				# 				for nota in notas:
				# 					if nota.nota:
				# 						media += int(nota.nota)
				# 					else:
				# 						n -= 1
				# 				if n != 0:
				# 					media = media/n
				# 				inscricao.media = media
				# 				inscricao.save()

				if 'proximo' in request.POST:
					return redirect('galeria_projeto', codigo=proximo.codigo, ordem=ordem)
				elif 'galeria' in request.POST:
					return redirect('galeria', ordem=ordem)
				else:
					return redirect('galeria_projeto', codigo=codigo, ordem=ordem)

			else:
				if not_juri(request.user):
					form = SelecaoForm(instance=inscricao)
					selecao_form = SelecaoJuriForm(instance=inscricao, label_suffix='')
					if inscricao.selecao:
						texto_form = TextoJuriForm(prefix='texto', instance=inscricao, label_suffix='')
					if selecionado:
						ordem_form = OrdemForm(instance=selecionado, label_suffix='')
				# else:
				# 	form = AvaliacaoForm(instance=juri, prefix='juri', label_suffix='')

	# paginacao
	page = request.GET.get('page', 1)
	if codigo:
		paginator = Paginator([inscricao], 1)
	else:
		paginator = Paginator(inscricoes, 10)
	try:
		pg = paginator.page(page)
	except PageNotAnInteger:
		pg = paginator.page(1)
	except EmptyPage:
		pg = paginator.page(paginator.num_pages)

	return render(request, 'o_t/galeria.html', {
		'edit': 'galeria_edit',
		'titulo': titulo, 
		'menu': menu, 
		'cartaz': cartaz,
		'inscricoes': inscricoes,
		'pg': pg,
		'form': form,
		'texto_form': texto_form,
		'selecao_form': selecao_form,
		'ordem_form': ordem_form,
		'ordem': ordem,
		# 'ativo':ativo,
		'proximo':proximo,
		})

@login_required
@user_passes_test(not_juri)
def galeria_dados(request):
	titulo = _('galeria')
	cartaz = Cartaz.objects.get_or_create(pagina='galeria')[0]
	inscricoes = Inscricao.objects.all()
	inscricoes_ = Inscricao.objects.exclude(finalizada=None)
	projeto = None
	dados = []
	palafitas = []
	for i, palafita in enumerate(Projeto.palafitas):
		finalizadas = Projeto.objects.filter(palafita=palafita[0], inscricao__in=inscricoes_).count()
		total = Projeto.objects.filter(palafita=palafita[0]).count()
		palafitas.append([palafita[1], finalizadas, total])
	paises = []
	pais = None
	for item in Dados.objects.all().order_by('pais'):
		if item.select_verbose() != pais:
			pais = item.select_verbose()
			finalizadas = Dados.objects.filter(pais=item.pais, inscricao__in=inscricoes_).count()
			total = Dados.objects.filter(pais=item.pais).count()
			paises.append([pais, finalizadas, total])
	dados.append(['paises', paises])
	dados.append(['palafitas', palafitas])

	return render(request, 'o_t/galeria_dados.html', {
		'titulo': titulo, 
		'menu': menu, 
		'cartaz': cartaz,
		'inscricoes': inscricoes,
		'projeto': projeto,
		'dados': dados,
		})

@login_required
@user_passes_test(not_juri)
def galeria_edit(request):
	titulo = _('galeria')
	cartaz = Cartaz.objects.get_or_create(pagina='galeria')[0]

	if request.method == 'POST':
		if 'cartaz_submit' in request.POST or 'cartaz_submit_home' in request.POST:
			cartaz_form = CartazForm(request.POST, request.FILES, instance=cartaz, prefix='cartaz')
			if cartaz_form.is_valid():
				cartaz_form.save()
				return redirect('galeria')
			criterios_form = CriteriosForm(prefix='criterios')
	else:
		cartaz_form = CartazForm(instance=cartaz, prefix='cartaz')

	return render(request, 'o_t/galeria_edit.html', {
		'titulo': titulo, 
		'menu': menu, 
		'cartaz': cartaz,
		'cartaz_form': cartaz_form,
		})

def blog(request, pk=None, slug=None, tag=None):
	titulo = 'blog'
	nota = None
	if pk:
		nota = get_object_or_404(Nota, pk=pk)
	elif slug:
		if Nota.objects.filter(slug_en=slug).exists():
			nota = get_object_or_404(Nota, slug_en=slug)
		else:
			nota = get_object_or_404(Nota, slug=slug)

	# tags
	tags = Tag.objects.all()
	if tag:
		if request.LANGUAGE_CODE == 'en' and Tag.objects.filter(tag_en=tag).exists():
			tag = get_object_or_404(Tag, tag_en=tag)
		else:
			tag = get_object_or_404(Tag, tag=tag)

	# notas lista
	# if rascunho:
	# 	notas = Nota.objects.exclude(data1__lte=timezone.now())
	if request.user.is_authenticated and not_juri(request.user):
		notas = Nota.objects.all().order_by(F('data1').desc(nulls_first=True))
	else:
		notas = Nota.objects.filter(data1__lte=timezone.now())
	if tag:
		notas = notas.filter(tags__in=[tag.pk])

	# paginacao
	page = request.GET.get('page', 1)
	paginator = Paginator(notas, 5)
	try:
		notas_pg = paginator.page(page)
	except PageNotAnInteger:
		notas_pg = paginator.page(1)
	except EmptyPage:
		notas_pg = paginator.page(paginator.num_pages)

	return render(request, 'o_t/blog.html', {
		'edit': 'nota_add',
		'edit_btn': 'novo post',
		'titulo': titulo, 
		'menu': menu, 
		'notas': notas,
		'nota': nota,
		'tags': tags,
		'tag': tag,
		'notas_pg': notas_pg,
		# 'rascunho': rascunho,
		})

@login_required
@user_passes_test(not_juri)
def blog_edit(request, pk=None):
	titulo = 'blog'
	nota = None
	nota_form = None
	imagem_form = None
	tag_form = None
	novatag_form = None
	if pk:
		nota = get_object_or_404(Nota, pk=pk)

	if request.method == 'POST':
		if 'nota_submit' in request.POST or 'nota_submit_home' in request.POST:
			if nota:
				data = Nota.objects.filter(pk=nota.pk).values()[0]
				nota_form = NotaForm(request.POST, instance=nota, prefix='nota', initial=data)
				imagem_form = ImagemForm(request.POST, request.FILES, instance=nota, prefix='img')
				if nota_form.is_valid() and imagem_form.is_valid():
					nota = nota_form.save(commit=False)
					if nota_form.has_changed():
						if 'titulo' in nota_form.changed_data:
							nota.slug = ''
						if 'titulo_en' in nota_form.changed_data:
							nota.slug_en = ''
					nota.save()
					nota_form.save_m2m()
					imagem_form.save()
					if 'nota_submit_home' in request.POST:
						return redirect('blog_slug', slug=nota.slug)
				imagem_form = ImagemForm(instance=nota, prefix='img')

			else:
				nota_form = NotaForm(request.POST, prefix='nota')
				if nota_form.is_valid():
					nota = nota_form.save(commit=False)
					nota.autor = request.user
					nota.save()
					nota_form.save_m2m()
					if 'nota_submit_home' in request.POST:
						return redirect('blog_slug', slug=nota.slug)
					else:
						return redirect('nota_edit', pk=nota.pk)
			tag_form = TagForm(prefix='tag')
		else:
			if 'tag_submit' in request.POST:
				tag_form = TagForm(request.POST, prefix='tag')
				if tag_form.is_valid():
					tag_form.save()
					tag_form = TagForm(prefix='tag')
			if nota:
				nota_form = NotaForm(instance=nota, prefix='nota')
				imagem_form = ImagemForm(instance=nota, prefix='img')
			else:
				nota_form = NotaForm(prefix='nota')
	else:
		if nota:
			nota_form = NotaForm(instance=nota, prefix='nota')
			imagem_form = ImagemForm(instance=nota, prefix='img')
		else:
			nota_form = NotaForm(prefix='nota')
		tag_form = TagForm(prefix='tag')

	return render(request, 'o_t/blog_edit.html', {
		'titulo': titulo, 
		'menu': menu, 
		'nota': nota,
		'nota_form': nota_form,
		'imagem_form': imagem_form,
		'tag_form': tag_form,
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


def faq(request, confirmacao=False, pk=None, slug=None):
	titulo = _('perguntas frequentes')
	consulta_form = None
	lang = get_language()

	if pk or slug:
		if pk:
			bloco = get_object_or_404(BlocoRespostas, pk=pk)
		if slug:
			if BlocoRespostas.objects.filter(slug_en=slug).exists():
				bloco = get_object_or_404(BlocoRespostas, slug_en=slug)
			else:
				bloco = get_object_or_404(BlocoRespostas, slug=slug)
		respostas = Pergunta.objects.filter(bloco=bloco)
	else:
		respostas = Faq.objects.filter(publicar=True)
	blocos = BlocoRespostas.objects.filter(data1__lte=timezone.now()).order_by('-data1')
	
	if request.method == 'POST':
		consulta_form = PerguntaForm(request.POST)
		if consulta_form.is_valid():
			pergunta = consulta_form.save(commit=False)
			pergunta.lang = request.LANGUAGE_CODE
			pergunta.save()
			# enviar email
			assunto = _('Outros Territórios_consulta')
			msg = msg_consulta.format(nome=pergunta.nome, consulta=pergunta.consulta)
			send_mail(assunto, msg, settings.EMAIL_HOST_USER, [pergunta.email,])
			return redirect('faq_confirmacao')
	else:
		consulta_form = PerguntaForm(label_suffix='')
	
	return render(request, 'o_t/faq.html', {
		'edit': 'faq_edit',
		'titulo': titulo, 
		'menu': menu, 
		'lang': lang,
		'consulta_form': consulta_form,
		'confirmacao': confirmacao,
		'respostas': respostas,
		'blocos': blocos,
		})

@login_required
@user_passes_test(not_juri)
def faq_edit(request, pk=None,):
	titulo = 'faq/edit'
	respostas = None
	faq = None
	bloco_form = None
	blocos = BlocoRespostas.objects.all()
	if pk:
		bloco = get_object_or_404(BlocoRespostas, pk=pk)
	
	if request.method == 'POST':
		if 'bloco_submit' in request.POST:
			novo_bloco = BlocoRespostasForm(request.POST, prefix='blocos')
			if novo_bloco.is_valid():
				novo_bloco.save()
		elif 'respostas_submit' in request.POST:
			data = BlocoRespostas.objects.filter(pk=bloco.pk).values()[0]
			bloco_form = BlocoRespostasForm(request.POST, instance=bloco, prefix='bloco', initial=data)
			respostas = RespostasForm(request.POST, queryset=Pergunta.objects.filter(bloco=bloco), prefix='respostas')
			if respostas.is_valid() and bloco_form.is_valid():
				bloco = bloco_form.save(commit=False)
				if bloco_form.has_changed():
					if 'nome' in bloco_form.changed_data:
						bloco.slug = ''
					if 'nome_en' in bloco_form.changed_data:
						bloco.slug_en = ''
				bloco.save()
				respostas.save()
		elif 'faq_submit' in request.POST or 'faq_submit_home' in request.POST:
			faq = FaqForm(request.POST, prefix='faq')
			if faq.is_valid():
				faq.save()
			if 'faq_submit_home' in request.POST:
				return redirect('faq')
		elif 'consultas_submit' in request.POST:
			consultas = ConsultasForm(request.POST, prefix='consultas')
			if consultas.is_valid():
				consultas.save()

	consultas = ConsultasForm(queryset=Pergunta.objects.filter(bloco__nome='rascunho'), prefix='consultas')
	novo_bloco = BlocoRespostasForm(prefix='blocos')
	if pk:
		respostas = RespostasForm(queryset=Pergunta.objects.filter(bloco=bloco), prefix='respostas')
		bloco_form = BlocoRespostasForm(instance=bloco, prefix='bloco')
	else:
		faq = FaqForm(prefix='faq')
	return render(request, 'o_t/faq_edit.html', {
		'titulo': titulo, 
		'menu': menu, 
		'consultas': consultas,
		'blocos': blocos,
		'novo_bloco': novo_bloco,
		'bloco_form': bloco_form,
		'respostas': respostas,
		'faq': faq,
		})

@login_required
def bloco_publish(request, pk):
	bloco = get_object_or_404(BlocoRespostas, pk=pk)
	consultas = Pergunta.objects.filter(bloco=bloco)
	lang = get_language()
	bloco.publish()
	# enviar email
	msgs = ()
	for pergunta in consultas:
		activate(pergunta.lang)
		assunto = _('Outros Territórios_resposta à consulta')
		link = request.build_absolute_uri(reverse('bloco_slug', kwargs={'slug': bloco.slug}))
		if pergunta.lang == 'en':
			resposta = pergunta.resposta_en
		else:
			resposta = pergunta.resposta
		msg = msg_publicacao_consulta.format(nome=pergunta.nome, consulta=pergunta.consulta, resposta=resposta, link=link)
		msg = assunto, msg, settings.EMAIL_HOST_USER, [pergunta.email,]
		msgs += (msg),
	send_mass_mail(msgs, fail_silently=False)
	activate(lang)
	return redirect('bloco_slug', slug=bloco.slug)

@login_required
def bloco_remove(request, pk):
    bloco = get_object_or_404(BlocoRespostas, pk=pk)
    bloco.delete()
    return redirect('faq_edit')

# def erro404(request, exception, template_name='404.html'):
#     return render(request, {'titulo':_('erro 404'), 'menu': menu,}, status=404)

# def erro500(request, template_name='500.html'):
#     return render(request, {'titulo':_('erro 500'), 'menu': menu,}, status=500)

