from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from templatesadmin import TemplatesAdminException
from templatesadmin.edithooks import TemplatesAdminHook

from mercurial import hg, ui, match
import os


TEMPLATESADMIN_HG_ROOT = getattr(
    settings,
    'TEMPLATESADMIN_HG_ROOT',
    None
)


class HgCommitHook(TemplatesAdminHook):
    '''
    Commit to git after saving
    '''

    @classmethod
    def post_save(cls, request, form, template_path):
        dir = os.path.dirname(template_path) + os.sep
        file = os.path.basename(template_path)

        if request.user.first_name and request.user.last_name:
            author = "%s %s" % (request.user.first_name, request.user.last_name)
        else:
            author = request.user.username

        message = form.cleaned_data['commitmessage'] or '--'

        repo_path = None
        for template_dir in settings.TEMPLATE_DIRS:
            if dir.startswith(template_dir):
                if repo_path is None or len(template_dir)>len(repo_path):
                    repo_path = template_dir
        if repo_path is None:
            raise TemplatesAdminException( _("Could not find template base directory") )
        commit_file = template_path
        if commit_file.startswith(path):
            commit_file = commit_file[len(path):]
            if commit_file.startswith("/"):
                commit_file = commit_file[1:]
        uio = ui.ui()
        uio.setconfig('ui', 'interactive', False)
        uio.setconfig('ui', 'report_untrusted', False)
        uio.setconfig('ui', 'quiet', True)
        repo = hg.repository(uio, path=repo_path)
        filter = match.match(repo.root, dir, [file])
        repo.commit(match=filter, text=message, user="%s <%s>" % (author, request.user.email))

        return "Template '%s' was committed succesfully into mercurial repository." % file

    @classmethod
    def contribute_to_form(cls, template_path):
        return dict(commitmessage=forms.CharField(
            widget=forms.Textarea(attrs={'rows':'5', 'cols': '40'}),
            label = _('Change message:'),
            required = True,
        ))
