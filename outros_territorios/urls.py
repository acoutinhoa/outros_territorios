from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view()),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
	# path('accounts/', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include('o_t.urls')),
    prefix_default_language=False
)

handler404 = 'o_t.views.erro404'
handler500 = 'o_t.views.erro500'