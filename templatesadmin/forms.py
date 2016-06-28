from django import forms
from django.forms.forms import DeclarativeFieldsMetaclass 
from .widgets import CodeMirrorEditor

class CodemirrorForm( forms.Form ):
    """
        Display the code using CodeMirror editor
    """
    content = forms.CharField(
        widget = forms.Textarea(attrs={'rows': 10, 'cols': 40})
    )

    def __init__(self, *args, **kwargs):
        syntax = kwargs.pop('widget_syntax') or 'htmlmixed'

        super(CodemirrorForm, self).__init__( *args, **kwargs )

        #
        # Overwrite editor field dynamically 
        # 
        self.fields['content'] =  forms.CharField(
            widget = CodeMirrorEditor(attrs={'syntax': syntax})
        )

class CodemirrorFormHtml( forms.Form ):
    content = forms.CharField(
        widget = CodeMirrorEditor(attrs={'syntax': 'htmlmixed'})
    )
