from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from trips.views import index
from trips.views import hello_world
from trips.views import TGOS
from trips.views import home

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', index),
	url(r'^admin/', include(admin.site.urls)),
    url(r'^demo/$', demo),
    url(r'^test/$', test),
    url(r'^TGOS/$', TGOS),
)
