from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import Nota


protocol = 'https'
i18n = True

class PostSitemap(Sitemap):    
    changefreq = 'monthly'
    priority = 0.5
    protocol = protocol
    i18n = i18n

    def items(self):
        return Nota.objects.filter(data1__lte=timezone.now())

    def lastmod(self, obj):
        return obj.data1

class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'
    protocol = protocol
    i18n = i18n

    def items(self):
        return ['home', 'concurso', 'galeria', 'blog', 'faq']

    def location(self, item):
        return reverse(item)

class ConcursoSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'
    protocol = protocol
    i18n = i18n

    def items(self):
        return [_('inscricoes'), _('arquivos'), _('cronograma'), _('juri')]

    def location(self, item):
        return '%s#%s/' % (reverse('concurso'), item)
