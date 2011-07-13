from django.conf.urls.defaults import patterns,url
from django.utils.functional import update_wrapper
from django.contrib.admin.sites import AdminSite

urlpatterns = patterns('',
    url(r'^$', 'templatesadmin.views.listing', name='templatesadmin-overview'),
    url(r'^edit/(?P<path>.*)/$', 'templatesadmin.views.modify', name='templatesadmin-edit'),
)
