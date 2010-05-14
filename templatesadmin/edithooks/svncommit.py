from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from templatesadmin import TemplatesAdminException
from templatesadmin.edithooks import TemplatesAdminHook

import pysvn
import os

class SvnCommitHook( TemplatesAdminHook ):
    '''
        Commit to svn after saving
    '''


    @classmethod
    def post_save(cls, request, form, template_path):
        dir, file = os.path.dirname(template_path) + "/", os.path.basename( template_path )

        if request.user.first_name and request.user.last_name and request.user.email:
            author = "%s %s <%s>" % ( request.user.first_name , request.user.last_name , request.user.email )
        else
            author = request.user.username

        message = (form.cleaned_data['commitmessage'] or '--') + '\n'
        message += '\n'

        # Get path for repository
        repo_path = None
        for template_dir in settings.TEMPLATE_DIRS:
            if dir.startswith(template_dir):
                if repo_path is None or len(template_dir) > len(repo_path):
                    repo_path = template_dir
        if repo_path is None:
            raise TemplatesAdminException(_("Could not find template base directory") )

        commit_file = template_path
        if commit_file.startswith(repo_path):
            commit_file = commit_file[len(repo_path):]
            if commit_file.startswith("/"):
                commit_file = commit_file[1:]

        svn = pysvn.Client() 
        svn.checkin( [str(commit_file)], message)

    @classmethod
    def contribute_to_form(cls, template_path):
        return dict(commitmessage=forms.CharField(
            widget=forms.TextInput(attrs={'size': '100'}),
            label = _("Change message"),
            required = False
        ))
