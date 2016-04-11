import os

from django.conf.urls import include, url
from django.contrib import admin

from .backend.views import *

SITE_MEDIA   = os.path.join(os.path.dirname(__file__), 'site_media')
STATIC_MEDIA = os.path.join(os.path.dirname(__file__), 'static')
urlpatterns = [
    # Examples:
    # url(r'^$', 'syracuse_crime.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

	url(r'^$', Home.as_view(), name='home'),
	url(r'map/$', HeatMap.as_view(), name='heat_map'),
	url(r'stats/$', Stats.as_view(), name='stats'),
	url(r'about/$', About.as_view(), name='about'),
	url(r'faq/$', FAQ.as_view(), name='faq'),

	url(r'site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': SITE_MEDIA, }),
	url(r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_MEDIA, }),
]
