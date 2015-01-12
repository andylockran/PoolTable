from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('PoolLeague.views',
    # Examples:
    # url(r'^$', 'PoolTable.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'home', name='home'),
)