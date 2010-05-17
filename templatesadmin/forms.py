from django import forms
from widgets import CodeMirrorEditor

class TemplateForm(forms.Form):
    content = forms.CharField(
        widget = forms.Textarea()
    )

class RichTemplateForm( forms.Form ):
    content = forms.CharField(
        widget = CodeMirrorEditor()
    )
