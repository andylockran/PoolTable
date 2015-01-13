from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PoolTable.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'PoolScores.views.home', name='home'),
    url(r'^score/$', 'PoolScores.views.score', name='score'),
    url(r'^league/', include('PoolLeague.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', include(admin.site.urls)),
)
