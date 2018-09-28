# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404, redirect
# from django.utils import timezone
# from django.urls import reverse, reverse_lazy
# from django.core.mail import BadHeaderError, send_mail
# from django.conf import settings
# from random import randint, randrange
# from .forms import *
# from .models import *


# menu = [
# 	['início', reverse_lazy('home'), []],
# 	['chamada de ideias', reverse_lazy('concurso'), [
# 		('inscrições', 'inscricoes'),
# 		('bases do concurso', 'bases'), 
# 		('cronograma', 'cronograma'), 
# 		('comissão julgadora', 'juri'),
# 		]],
# 	['galeria', reverse_lazy('galeria'), []],
# 	['blog', reverse_lazy('blog'), []],
# 	['faq', reverse_lazy('faq'), []],
# 	]

# msg_inscricao = '''olá %s,
# mensagem de confirmacao de inscrição.
# _
# link para envio do projeto:
# %s'''

# msg_email = '''olá %s,
# reenvio de link para inscricao.
# _
# link para envio do projeto:
# %s'''

# msg_consulta = '''olá %s,
# mensagem de confirmacao.
# _
# consulta:
# %s'''



# def home(
# 	request, 
# 	edit = False, 
# 	pk = 1,
# 	titulo = 'home',
# 	form = None,
# 	formset = None,
# 	):
# 	cartaz = get_object_or_404(Cartaz, pk=pk)
# 	img = cartaz.arquivo_set.all().order_by('?')[0]
# 	notas = Nota.objects.filter(data1__lte=timezone.now()).order_by('-data1')

# 	if edit:
# 		if request.method == 'POST':
# 			form = CartazForm(request.POST, request.FILES, instance=cartaz)
# 			formset = ArquivoFormSet(request.POST, request.FILES, instance=cartaz)
# 			if formset.is_valid() and form.is_valid():
# 				cartaz = form.save()
# 				formset.save()
# 				return redirect('home')
# 		else:
# 			form = CartazForm(instance=cartaz)
# 			formset = ArquivoFormSet(instance=cartaz)

# 	return render(request, 'o_t/home.html', {
# 		'titulo': titulo, 
# 		'menu': menu, 
# 		'borda': def_borda(),
# 		'cartaz': cartaz,
# 		'img': img,
# 		'notas': notas,
# 		'form': form,
# 		'formset': formset,
# 		})


# def concurso(
# 	request, 
# 	edit = False, 
# 	pk = 2,
# 	confirmacao = False,
# 	):
# 	titulo = 'concurso'
# 	cartaz_form = None
# 	arquivos_form = None
# 	juri_form = None
# 	inscricao_form = None
# 	dados_form = None
# 	email_form = None
# 	cartaz = get_object_or_404(Cartaz, pk=pk)
# 	arquivos = cartaz.arquivo_set.all()
# 	jurados = Juri.objects.all()

# 	if edit:
# 		if request.method == 'POST':
# 			if 'juri_submit' in request.POST:
# 				juri_form = JuriFormSet(request.POST, prefix='juri')
# 				if juri_form.is_valid():
# 					juri_form.save()
# 			elif 'cartaz_submit' in request.POST:
# 				cartaz_form = CartazForm(request.POST, instance=cartaz, prefix='cartaz')
# 				arquivos_form = ArquivoFormSet(request.POST, request.FILES, instance=cartaz, prefix='arquivo')
# 				if arquivos_form.is_valid() and cartaz_form.is_valid():
# 					cartaz = cartaz_form.save()
# 					arquivos_form.save()
# 			return redirect('concurso_edit')
# 		else:
# 			cartaz_form = CartazForm(instance=cartaz, prefix='cartaz')
# 			arquivos_form = ArquivoFormSet(instance=cartaz, prefix='arquivo')
# 			juri_form = JuriFormSet(prefix='juri')
# 	else:
# 		if request.method == 'POST':
# 			if 'inscricao_submit' in request.POST:
# 				inscricao_form = InscricaoForm(request.POST, prefix='inscricao')
# 				dados_form = DadosForm(request.POST, prefix='dados')
# 				if inscricao_form.is_valid() and dados_form.is_valid():
# 					inscricao = inscricao_form.save()
# 					dados = dados_form.save(commit=False)
# 					dados.inscricao = inscricao
# 					dados.save()
# 					# enviar email
# 					assunto = 'outros_territorios/inscrições'
# 					link = request.build_absolute_uri(reverse('inscricoes', kwargs={'pk': inscricao.pk}))
# 					msg = msg_inscricao % (inscricao.nome, link)
# 					send_mail(assunto, msg, settings.EMAIL_HOST_USER, [inscricao.email,])
# 					return redirect('inscricoes', pk=inscricao.pk)
# 			elif 'email_submit' in request.POST:
# 				email_form = EmailForm(request.POST, prefix='email')
# 				if email_form.is_valid():
# 					email = email_form.cleaned_data['email']
# 					inscricao = Inscricao.objects.get(email=email)
# 					# enviar email
# 					assunto = 'outros_territorios/link para inscrição'
# 					link = request.build_absolute_uri(reverse('inscricoes', kwargs={'pk': inscricao.pk}))
# 					msg = msg_email % (inscricao.nome, link)
# 					send_mail(assunto, msg, settings.EMAIL_HOST_USER, [inscricao.email,])
# 					return redirect('email_confirmacao')
# 		else:
# 			inscricao_form = InscricaoForm(prefix='inscricao')
# 			dados_form = DadosForm(prefix='dados')
# 			email_form = EmailForm(prefix='email')

# 	return render(request, 'o_t/concurso.html', {
# 		'titulo': titulo, 
# 		'menu': menu, 
# 		'borda': def_borda(),
# 		'cartaz': cartaz,
# 		'arquivos': arquivos,
# 		'cartaz_form': cartaz_form,
# 		'arquivos_form': arquivos_form,
# 		'juri_form': juri_form,
# 		'jurados': jurados,
# 		'inscricao_form': inscricao_form,
# 		'dados_form': dados_form,
# 		'email_form': email_form,
# 		'confirmacao': confirmacao,
# 		})

# def inscricoes(
# 	request,
# 	pk,
# 	titulo = 'inscricoes',
# 	):
# 	inscricao = get_object_or_404(Inscricao, pk=pk)
# 	dados = Dados.objects.get(inscricao=inscricao)
# 	inscricao_form = InscricaoForm(instance=inscricao, prefix='inscricao')
# 	dados_form = DadosForm(instance=dados, prefix='dados')

# 	if request.method == 'POST':
# 		if 'equipe_submit' in request.POST:
# 			equipe_form = EquipeFormSet(request.POST, instance=inscricao, prefix='equipe')
# 			if equipe_form.is_valid():
# 				equipe_form.save()
# 		elif 'projeto_submit' in request.POST:
# 			projeto_form = ProjetoForm(request.POST, request.FILES, instance=inscricao, prefix='projeto')
# 			prancha_form = PranchaFormSet(request.POST, request.FILES, instance=inscricao, prefix='prancha')
# 			if projeto_form.is_valid() and prancha_form.is_valid():
# 				projeto_form.save()
# 				prancha_form.save()
# 		return redirect('inscricoes', pk=pk)
# 	else:
# 		equipe_form = EquipeFormSet(instance=inscricao, prefix='equipe')
# 		projeto_form = ProjetoForm(instance=inscricao, prefix='projeto')
# 		prancha_form = PranchaFormSet(instance=inscricao, prefix='prancha')

# 	return render(request, 'o_t/inscricoes.html', {
# 		'titulo': titulo, 
# 		'inscricao': inscricao, 
# 		'inscricao_form': inscricao_form,
# 		'dados_form': dados_form,
# 		'equipe_form': equipe_form,
# 		'projeto_form': projeto_form,
# 		'prancha_form': prancha_form,
# 		})

# def galeria(
# 	request,
# 	titulo = 'galeria',
# 	):
# 	return render(request, 'o_t/galeria.html', {
# 		'titulo': titulo, 
# 		'menu': menu, 
# 		'borda': def_borda(),
# 		})

# def blog(
# 	request, 
# 	pk = None, 
# 	edit = False,
# 	titulo = 'blog',
# 	nota = None,
# 	form = None,
# 	):
# 	notas = Nota.objects.filter(data1__lte=timezone.now()).order_by('-data1')
# 	notas_ = Nota.objects.exclude(data1__lte=timezone.now()).order_by('-data0')
# 	if pk:
# 		nota = get_object_or_404(Nota, pk=pk)

# 	if edit:
# 		if request.method == 'POST':
# 			form = NotaForm(request.POST, request.FILES, instance=nota)
# 			if form.is_valid():
# 				nota = form.save(commit=False)
# 				nota.autor = request.user
# 				nota.save()
# 				return redirect('blog', pk=nota.pk)
# 		else:
# 			form = NotaForm(instance=nota)

# 	return render(request, 'o_t/blog.html', {
# 		'titulo': titulo, 
# 		'menu': menu, 
# 		'borda': def_borda(),
# 		'notas': notas,
# 		'notas_': notas_,
# 		'nota': nota,
# 		'form': form,
# 		})

# @login_required
# def nota_publish(request, pk):
#     nota = get_object_or_404(Nota, pk=pk)
#     nota.publish()
#     return redirect('blog', pk=pk)

# @login_required
# def nota_remove(request, pk):
#     nota = get_object_or_404(Nota, pk=pk)
#     nota.delete()
#     return redirect('blog')


# def faq(
# 	request, 
# 	confirmacao = False,
# 	titulo = 'faq',
# 	form = None,
# 	pk = None,
# 	):
# 	if pk:
# 		bloco = get_object_or_404(BlocoRespostas, pk=pk)
# 		respostas = Pergunta.objects.filter(bloco=bloco)
# 	else:
# 		respostas = Faq.objects.filter(publicar=True)
# 	blocos = BlocoRespostas.objects.filter(data1__lte=timezone.now()).order_by('-data1')
	
# 	if request.method == 'POST':
# 		form = PerguntaForm(request.POST)
# 		if form.is_valid():
# 			pergunta = form.save(commit=False)
# 			pergunta.data = timezone.now()
# 			pergunta.save()
# 			# enviar email
# 			assunto = 'outros_territorios/consultas'
# 			msg = msg_consulta % (pergunta.nome, pergunta.consulta)
# 			send_mail(assunto, msg, settings.EMAIL_HOST_USER, [pergunta.email,])
# 			return redirect('faq_confirmacao')
# 	else:
# 		form = PerguntaForm()
	
# 	return render(request, 'o_t/faq.html', {
# 		'titulo': titulo, 
# 		'menu': menu, 
# 		'borda': def_borda(),
# 		'form': form,
# 		'confirmacao': confirmacao,
# 		'respostas': respostas,
# 		'blocos': blocos,
# 		})

# @login_required
# def faq_edit(request, pk=None,):
# 	titulo = 'faq/edit'
# 	respostas = None
# 	faq = None
# 	blocos = BlocoRespostas.objects.all()
# 	if pk:
# 		bloco = get_object_or_404(BlocoRespostas, pk=pk)
	
# 	if request.method == 'POST':
# 		if 'bloco_submit' in request.POST:
# 			novo_bloco = BlocoRespostasForm(request.POST, prefix='blocos')
# 			if novo_bloco.is_valid():
# 				novo_bloco.save()
# 		elif 'respostas_submit' in request.POST:
# 			respostas = RespostasFormSet(request.POST, queryset=Pergunta.objects.filter(bloco=bloco), prefix='respostas')
# 			if respostas.is_valid():
# 				respostas.save()
# 		elif 'faq_submit' in request.POST:
# 			faq = FaqFormSet(request.POST, prefix='faq')
# 			if faq.is_valid():
# 				faq.save()
# 		elif 'consultas_submit' in request.POST:
# 			consultas = ConsultasFormSet(request.POST, prefix='consultas')
# 			if consultas.is_valid():
# 				consultas.save()

# 	consultas = ConsultasFormSet(queryset=Pergunta.objects.filter(bloco__nome='rascunho'), prefix='consultas')
# 	novo_bloco = BlocoRespostasForm(prefix='blocos')
# 	if pk:
# 		respostas = RespostasFormSet(queryset=Pergunta.objects.filter(bloco=bloco), prefix='respostas')
# 	else:
# 		faq = FaqFormSet(prefix='faq')
# 	return render(request, 'o_t/faq_edit.html', {
# 		'titulo': titulo, 
# 		'menu': menu, 
# 		'borda': def_borda(),
# 		'consultas': consultas,
# 		'blocos': blocos,
# 		'novo_bloco':novo_bloco,
# 		'respostas': respostas,
# 		'faq': faq,
# 		})

# @login_required
# def bloco_publish(request, pk):
#     bloco = get_object_or_404(BlocoRespostas, pk=pk)
#     bloco.publish()
#     return redirect('faq_edit')

# @login_required
# def bloco_remove(request, pk):
#     bloco = get_object_or_404(BlocoRespostas, pk=pk)
#     bloco.delete()
#     return redirect('faq_edit')

# ################### funcoes


# def def_randomiza(lista):
# 	l = []
# 	for i in range(len(lista)):
# 		l.append(lista.pop(randrange(len(lista))))
# 	return l

# def def_borda(x=5, y=25):
# 	return str(randint(x, y)) + 'px'


# # def send_email(request, slug):
# #     """ Send notification email to original owner of device who lost it """
# #     grab = Item.objects.get(slug=slug)
# #     if request.method == "POST":
# #         form = NotifyEmailForm(request.POST)
# #         if form.is_valid():
# #             subject = form.cleaned_data['subject']
# #             message = form.cleaned_data['message']
# #             sender = request.user.email
# #             recipients = [grab.created_by.email]
# #             recipients.append(sender)
 
# #             send_mail(subject, message, sender, recipients)
# #             return HttpResponseRedirect('/notify/thanks')  # Redirect after POST
# #     else:
# #         form = NotifyEmailForm()  # An unbound form
# #     return render(request, 'send-mail.html', {'form': form, 'object': slug, })


# # def send_email(request):
# #     subject = request.POST.get('subject', '')
# #     message = request.POST.get('message', '')
# #     from_email = request.POST.get('from_email', '')
# #     if subject and message and from_email:
# #         try:
# #             send_mail(subject, message, from_email, ['admin@example.com'])
# #         except BadHeaderError:
# #             return HttpResponse('Invalid header found.')
# #         return HttpResponseRedirect('/contact/thanks/')
# #     else:
# #         # In reality we'd use a form class
# #         # to get proper validation errors.
# #         return HttpResponse('Make sure all fields are entered and valid.')

