from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from . import views

blog_patterns = [
    path('', views.blog, name='blog'),
    path('add/', views.blog, {'edit':True,}, name='nota_add'),
    path('tag/<slug:tag>/', views.blog, name='blog_tag'),
    path('<int:pk>/', views.blog, name='blog'),
    path('<int:pk>/edit/', views.blog, {'edit':True,}, name='nota_edit'),
    path('<int:pk>/publish/', views.nota_publish, name='nota_publish'),
    path('<int:pk>/remove/', views.nota_remove, name='nota_remove'),
    path('<slug:slug>/', views.blog, name='blog_slug'),
]

faq_patterns = [
    path('', views.faq, name='faq'),
    path('<int:pk>/', views.faq, name='faq'),
    path('ok/', views.faq, {'confirmacao':True,}, name='faq_confirmacao'),
    path('edit/', views.faq_edit, name='faq_edit'),
    path('<int:pk>/edit/', views.faq_edit, name='faq_edit'),
    path('<int:pk>/publish/', views.bloco_publish, name='bloco_publish'),
    path('<int:pk>/remove/', views.bloco_remove, name='bloco_remove'),
    path('<slug:slug>/', views.faq, name='bloco_slug'),
]

concurso_patterns = [
    path('', views.concurso, name='concurso'),
    path('edit/', views.concurso, {'edit':True,}, name='concurso_edit'),
    path('ok/', views.concurso, {'confirmacao':True,}, name='email_confirmacao'),
    path(_('inscricoes/<uuid:pk>/'), views.inscricoes, name='inscricoes'),
    path(_('inscricoes/<uuid:pk>/submit'), views.inscricoes_submit, name='inscricoes_submit'),
    path(_('inscricoes/<uuid:pk>/erro'), views.inscricoes, {'erro':True,}, name='inscricoes_erro'),
]

galeria_patterns = [
    path('', views.galeria, name='galeria'),
    path('edit/', views.galeria, {'edit':True,}, name='galeria_edit'),
]

urlpatterns = [
    path('', views.home, name='home'),
    path('edit/', views.home, {'edit':True,}, name='home_edit'),

    path(_('galeria/'), include(galeria_patterns)),

    path(_('chamada_de_projetos/'), include(concurso_patterns)),
    path(_('perguntas_frequentes/'), include(faq_patterns)),
    path('blog/', include(blog_patterns)),
]


