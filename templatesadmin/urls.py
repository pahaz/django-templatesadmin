from django.conf.urls.defaults import patterns,url
from django.utils.functional import update_wrapper
from django.contrib.admin.sites import AdminSite

urlpatterns = patterns('',
    url(r'^$', 'templatesadmin.views.overview', name='templatesadmin-overview'),
    url(r'^edit/(?P<path>.*)/$', 'templatesadmin.views.edit', name='templatesadmin-edit'),
)
