from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.core.mail import BadHeaderError, send_mail, send_mass_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from random import randint, randrange, choice
from .forms import *
from .models import *

menu = [
	[_('início'), reverse_lazy('home'), []],
	[_('chamada de projetos'), reverse_lazy('concurso'), [
		(_('inscrições'), _('inscricoes')),
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


def home(request):
	titulo = _('início')
	cartaz = Cartaz.objects.get_or_create(pagina='home')[0]
	notas = Nota.objects.filter(data1__lte=timezone.now())
	# logos
	logos = Cartaz.objects.get_or_create(pagina='logos')[0]
	logos = Arquivo.objects.filter(pagina=logos)
	# img
	if cartaz.arquivo_set.all().exists():
		img = cartaz.arquivo_set.all().order_by('?')[0]
	else:
		img = None

	return render(request, 'o_t/home.html', {
		'titulo': titulo, 
		'menu': menu, 
		'logos': logos,
		'cartaz': cartaz,
		'img': img,
		'notas': notas,
	})

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

def concurso(request, confirmacao=False,):
	titulo = _('chamada de projetos')
	cartaz = Cartaz.objects.get_or_create(pagina='concurso')[0]
	arquivos = None
	if cartaz.arquivo_set.all().exists():
		arquivos = cartaz.arquivo_set.all()
	jurados = Juri.objects.all()

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
				return redirect('inscricoes', pk=inscricao.pk)
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
				return redirect('email_confirmacao')
			inscricao_form = InscricaoForm(prefix='inscricao', label_suffix='')
			dados_form = DadosForm(prefix='dados', label_suffix='')
	else:
		inscricao_form = InscricaoForm(prefix='inscricao', label_suffix='')
		dados_form = DadosForm(prefix='dados', label_suffix='')
		email_form = EmailForm(prefix='email', label_suffix='')

	return render(request, 'o_t/concurso.html', {
		'titulo': titulo, 
		'menu': menu, 
		'cartaz': cartaz,
		'arquivos': arquivos,
		'jurados': jurados,
		'inscricao_form': inscricao_form,
		'dados_form': dados_form,
		'email_form': email_form,
		'confirmacao': confirmacao,
	})

def concurso_edit(request):
	titulo = _('chamada de projetos')
	cartaz = Cartaz.objects.get_or_create(pagina='concurso')[0]

	if request.method == 'POST':
		if 'juri_submit' in request.POST or 'juri_submit_home' in request.POST:
			juri_form = JuriForm(request.POST, prefix='juri')
			if juri_form.is_valid():
				juri_form.save()
				if 'juri_submit_home' in request.POST:
					return redirect('concurso')
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
	else:
		cartaz_form = CartazForm(instance=cartaz, prefix='cartaz')
		arquivos_form = ArquivoForm(instance=cartaz, prefix='arquivo')
		juri_form = JuriForm(prefix='juri')

	return render(request, 'o_t/concurso_edit.html', {
		'titulo': titulo, 
		'menu': menu, 
		'cartaz_form': cartaz_form,
		'arquivos_form': arquivos_form,
		'juri_form': juri_form,
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

	if erro:
		erro = _('Você precisa preencher todos os campos do projeto para finalizar sua inscrição.')

	if request.method == 'POST':
		if 'equipe_submit' in request.POST:
			projeto_form = ProjetoForm(instance=projeto, prefix='projeto')
			equipe_form = EquipeForm(request.POST, instance=inscricao, prefix='equipe')
			if equipe_form.is_valid():
				equipe_form.save()
		elif 'projeto_submit' in request.POST:
			equipe_form = EquipeForm(instance=inscricao, prefix='equipe')
			projeto_form = ProjetoForm(request.POST, request.FILES, instance=projeto, prefix='projeto')
			if projeto_form.is_valid():
				projeto_form.save()
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
	})

def inscricoes_submit(request, pk,):
	inscricao = get_object_or_404(Inscricao, pk=pk)
	projeto = Projeto.objects.get(inscricao=inscricao)

	if projeto.palafita and projeto.nome and projeto.texto and projeto.img and projeto.arquivo:
		inscricao.finaliza()
		return redirect('inscricoes', pk=pk)
	else:
		return redirect('inscricoes_erro', pk=pk)

def galeria(request, edit=False,):
	titulo = _('galeria')
	cartaz = Cartaz.objects.get_or_create(pagina='galeria')[0]
	cartaz_form = None

	if edit:
		if request.method == 'POST':
			if 'cartaz_submit' in request.POST or 'cartaz_submit_home' in request.POST:
				cartaz_form = CartazForm(request.POST, request.FILES, instance=cartaz)
				if cartaz_form.is_valid():
					cartaz_form.save()
			return redirect('galeria')
		else:
			cartaz_form = CartazForm(instance=cartaz)

	return render(request, 'o_t/galeria.html', {
		'titulo': titulo, 
		'menu': menu, 
		'edit': edit,
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
	if request.user.is_authenticated:
		notas = Nota.objects.all()
	else:
		notas = Nota.objects.filter(data1__lte=timezone.now())
	if tag:
		notas = notas.filter(tags__in=[tag.pk])


	return render(request, 'o_t/blog.html', {
		'titulo': titulo, 
		'menu': menu, 
		'notas': notas,
		'nota': nota,
		'tags': tags,
		})

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
			novatag_form = NovaTagForm(prefix='novatag')
		else:
			if 'tag_submit' in request.POST:
				tag_form = TagForm(request.POST, prefix='tag')
				if tag_form.is_valid():
					tag_form.save()
					tag_form = TagForm(prefix='tag')
				novatag_form = NovaTagForm(prefix='novatag')
			elif 'novatag_submit' in request.POST:
				novatag_form = NovaTagForm(request.POST, prefix='novatag')
				if novatag_form.is_valid():
					novatag_form.save()
					novatag_form = NovaTagForm(prefix='novatag')
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
		novatag_form = NovaTagForm(prefix='novatag')

	return render(request, 'o_t/blog_edit.html', {
		'titulo': titulo, 
		'menu': menu, 
		'nota': nota,
		'nota_form': nota_form,
		'imagem_form': imagem_form,
		'tag_form': tag_form,
		'novatag_form': novatag_form,
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
			pergunta = consulta_form.save()
			# enviar email
			assunto = _('Outros Territórios_consulta')
			msg = msg_consulta.format(nome=pergunta.nome, consulta=pergunta.consulta)
			send_mail(assunto, msg, settings.EMAIL_HOST_USER, [pergunta.email,])
			return redirect('faq_confirmacao')
	else:
		consulta_form = PerguntaForm(label_suffix='')
	
	return render(request, 'o_t/faq.html', {
		'titulo': titulo, 
		'menu': menu, 
		'consulta_form': consulta_form,
		'confirmacao': confirmacao,
		'respostas': respostas,
		'blocos': blocos,
		})

@login_required
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
	# enviar email
	assunto = _('Outros Territórios_resposta à consulta')
	link = request.build_absolute_uri(reverse('faq', kwargs={'pk': pk}))
	msgs = ()
	for pergunta in consultas:
		msg = msg_publicacao_consulta.format(nome=pergunta.nome, consulta=pergunta.consulta, resposta=pergunta.resposta, link=link)
		msg = assunto, msg, settings.EMAIL_HOST_USER, [pergunta.email,]
		msgs += (msg),
	send_mass_mail(msgs, fail_silently=False)
	bloco.publish()
	return redirect('faq', pk=pk)

@login_required
def bloco_remove(request, pk):
    bloco = get_object_or_404(BlocoRespostas, pk=pk)
    bloco.delete()
    return redirect('faq_edit')

def handler404(request, exception,):
    return render(request, 'error/404.html', {'titulo':'404', 'menu': menu,})

def handler500(request,):
    return render(request, 'error/500.html', {'titulo':'500', 'menu': menu,})
