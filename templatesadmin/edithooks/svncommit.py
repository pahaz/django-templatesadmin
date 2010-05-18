from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from templatesadmin import TemplatesAdminException
from templatesadmin.edithooks import TemplatesAdminHook

import os,re
import tempfile , subprocess

class SvnCommitHook( TemplatesAdminHook ):
    '''
        Commit to svn after saving
    '''

    @classmethod
    def post_save(cls, request, form, template_path):
        dir, file = os.path.dirname(template_path) + "/", os.path.basename( template_path )

        if request.user.first_name and request.user.last_name and request.user.email:
            author = "%s %s <%s>" % ( request.user.first_name , request.user.last_name , request.user.email )
        else:
            author = request.user.username

        # Avoid svn complaining about mixed dos(crlf) and unix(lf) line-ending 
        message = re.sub('\r\n', '\n', (form.cleaned_data['commitmessage'] or '--') )

        # Write commit-message to a temp-file
        commit_tmp_file     =  tempfile.NamedTemporaryFile()
        try:
            commit_msg_file     =  commit_tmp_file.name

            message = (message + '\nCommited in admin by: ' + author ).encode('utf-8')
            commit_tmp_file.write( message )
            commit_tmp_file.flush()

            # Stolen from gitpython's git/cmd.py
            command = 'svn commit -F %(commit_msg_file)s %(file)s' % locals()
            proc = subprocess.Popen(
                args=command,
                shell=True,
                cwd=dir,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            try:
                stderr_value = proc.stderr.read()
                stdout_value = proc.stdout.read()
                status = proc.wait()
            finally:
                proc.stderr.close()

            if status != 0:
                raise TemplatesAdminException("Error while executing %s: %s" % (command, stderr_value.rstrip(), ))

            return stdout_value.rstrip()

        finally:
            # Close and delete commit-message file. 
            commit_tmp_file.close()

    @classmethod
    def contribute_to_form(cls, template_path):
        return dict(commitmessage=forms.CharField(
            widget=forms.Textarea(attrs={'rows': '5', 'cols': '40'}),
            label = _("Change message:"),
            required = True 
        ))
