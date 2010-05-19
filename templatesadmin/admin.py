from django.contrib import admin
from django.conf.urls.defaults import patterns,url
from django.utils.functional import update_wrapper

from templatesadmin.models import FakeTemplateModel
from templatesadmin.views import overview, edit

class TemplatesAdmin(admin.ModelAdmin):
    """
        Admin for TemplatesAdmin
    """
    model = FakeTemplateModel 

    def add_view(self, request):
        pass

    def changelist_view(self, request ): 
        print "Hallo"
        return overview(request)

    def get_urls(self):

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urls = super(TemplatesAdmin,self).get_urls()
        # Instead of replacing templates, let's just replace this:
        info = self.model._meta.app_label, self.model._meta.module_name

        templatesadmin_urls = patterns('',
            url(r'^templates/$',                  wrap(overview), name='templatesadmin-overview'), 
            url(r'^templates/edit(?P<path>.*)/$', wrap(edit),     name='templatesadmin-edit'), 
        ) 

        return urls + templatesadmin_urls

admin.site.register(FakeTemplateModel, TemplatesAdmin)
