from django.contrib.admin.sites import AdminSite
from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^$', 'templatesadmin.views.overview', name='templatesadmin-overview'),
    url(r'^edit/(?P<path>.*)/$', 'templatesadmin.views.edit', name='templatesadmin-edit'),
)
