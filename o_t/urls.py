# from django.urls import include, path
# from . import views

# blog_patterns = [
#     path('', views.blog, name='blog'),
#     path('<int:pk>/', views.blog, name='blog'),
#     path('add/', views.blog, {'edit':True,}, name='nota_add'),
#     path('<int:pk>/edit/', views.blog, {'edit':True,}, name='nota_edit'),
#     path('<int:pk>/publish/', views.nota_publish, name='nota_publish'),
#     path('<int:pk>/remove/', views.nota_remove, name='nota_remove'),
# ]

# faq_patterns = [
#     path('', views.faq, name='faq'),
#     path('<int:pk>/', views.faq, name='faq'),
#     path('confirmacao/', views.faq, {'confirmacao':True,}, name='faq_confirmacao'),
#     path('edit/', views.faq_edit, name='faq_edit'),
#     path('<int:pk>/edit/', views.faq_edit, name='faq_edit'),
#     path('<int:pk>/publish/', views.bloco_publish, name='bloco_publish'),
#     path('<int:pk>/remove/', views.bloco_remove, name='bloco_remove'),
# ]

# concurso_patterns = [
#     path('', views.concurso, name='concurso'),
#     path('edit/', views.concurso, {'edit':True,}, name='concurso_edit'),
#     path('confirmacao/', views.concurso, {'confirmacao':True,}, name='email_confirmacao'),
#     path('inscricoes/<uuid:pk>', views.inscricoes, name='inscricoes'),
# ]

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('edit/', views.home, {'edit':True,}, name='home_edit'),

#     path('galeria/', views.galeria, name='galeria'),

#     path('concurso/', include(concurso_patterns)),
#     path('faq/', include(faq_patterns)),
#     path('blog/', include(blog_patterns)),
# ]


