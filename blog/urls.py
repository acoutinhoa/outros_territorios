from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),

    path('resumo/<int:pk>/', views.resumo, name='resumo'),
    path('resumo/<int:pk>/edit/', views.resumo_edit, name='resumo_edit'),

    path('blog/', views.post_list, name='post_list'),
    path('blog/<int:pk>/', views.post_detail, name='post_detail'),
    path('blog/new', views.post_new, name='post_new'),
    path('blog/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/', views.post_draft_list, name='post_draft_list'),
	path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
	path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


