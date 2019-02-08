from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

sitemaps = {
    'static': StaticViewSitemap,
    'concurso': ConcursoSitemap,
    'posts': PostSitemap,
}

blog_patterns = [
    path('', views.blog, name='blog'),
    path('add/', views.blog_edit, name='nota_add'),
    path('tag/<slug:tag>/', views.blog, name='blog_tag'),
    path('<int:pk>/', views.blog, name='blog'),
    # path('rascunhos/', views.blog, {'rascunho':True}, name='blog_rascunhos'),
    # path('rascunhos/<int:pk>/', views.blog, {'rascunho':True}, name='blog'),
    path('<int:pk>/edit/', views.blog_edit, name='nota_edit'),
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
    path('edit/', views.concurso_edit, name='concurso_edit'),
    path(_('inscricoes/email/'), views.email, name='email'),
    path(_('inscricoes/<uuid:pk>/'), views.inscricoes, name='inscricoes'),
    path(_('inscricoes/<uuid:pk>/submit'), views.inscricoes_submit, name='inscricoes_submit'),
    path(_('inscricoes/<uuid:pk>/erro'), views.inscricoes, {'erro':True,}, name='inscricoes_erro'),
    path('<slug:msg>/', views.concurso, name='confirmacao'),
]

galeria_patterns = [
    path('', views.galeria, name='galeria'),
    path('edit/', views.galeria_edit, name='galeria_edit'),
    path('<int:codigo>/', views.galeria, name='galeria_projeto'),
    path('dados/', views.galeria_dados, name='galeria_dados'),
    path('ordem/<slug:ordem>/', views.galeria, name='galeria'),
]

urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps' : sitemaps } , name='sitemap'),
    path('', views.home, name='home'),
    path('edit/', views.home_edit, name='home_edit'),

    path(_('galeria/'), include(galeria_patterns)),
    path(_('chamada_de_projetos/'), include(concurso_patterns)),
    path(_('perguntas_frequentes/'), include(faq_patterns)),
    path('blog/', include(blog_patterns)),
]

