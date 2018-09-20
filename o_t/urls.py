from django.urls import include, path
from . import views

blog_patterns = [
    path('', views.blog, name='blog'),
    path('<int:pk>/', views.blog, name='blog'),
    path('add/', views.blog, {'edit':True,}, name='nota_add'),
    path('<int:pk>/edit/', views.blog, {'edit':True,}, name='nota_edit'),
    path('<int:pk>/publish/', views.nota_publish, name='nota_publish'),
    path('<int:pk>/remove/', views.nota_remove, name='nota_remove'),
]

urlpatterns = [
    path('', views.home, name='home'),
    path('cartaz/', views.home, {'edit':True,}, name='cartaz_edit'),

    path('concurso/', views.concurso, name='concurso'),
    path('galeria/', views.galeria, name='galeria'),
    path('faq/', views.faq, name='faq'),
    path('blog/', include(blog_patterns)),
]


