from django import forms
from django.forms.forms import DeclarativeFieldsMetaclass 
from widgets import CodeMirrorEditor

class TemplateForm(forms.Form):
    content = forms.CharField(
        widget = forms.Textarea(attrs={'rows': 10, 'cols': 40})
    )

    def __init__(self, *args, **kwargs):
        """
            Backward compatibility for RichTemplateForm
        """
        kwargs.pop('widget_syntax')

        super(TemplateForm, self).__init__( *args, **kwargs)
        print self.fields


class RichTemplateForm( forms.Form ):
    """
        Display the code using CodeMirror editor
    """
    content = forms.CharField(
        widget = forms.Textarea(attrs={'rows': 10, 'cols': 40})
    )

    def __init__(self, *args, **kwargs):
        syntax = kwargs.pop('widget_syntax') or 'dummy' 

        super(RichTemplateForm, self).__init__( *args, **kwargs )

        #
        # Overwrite editor field dynamically 
        # 
        self.fields['content'] =  forms.CharField(
            widget = CodeMirrorEditor(attrs={'syntax': syntax})
        ) 
