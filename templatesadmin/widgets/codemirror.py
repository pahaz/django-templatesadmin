from django import forms
from django.conf import settings

from django.utils.safestring import mark_safe
from django.utils.html       import escape, conditional_escape
from django.utils.encoding   import StrAndUnicode, force_unicode

from django.forms.util import flatatt
from urlparse import urljoin 

class CodeMirrorEditor( forms.Textarea ):
    """
        CodeMirror rich-editor in HTML (provides syntax highlight and
        other some basic things.)

        http://marijn.haverbeke.nl/codemirror/manual.html
    """

    CODEEDITOR_JS = """
<script type="text/javascript">
    window.onload = function(e){
        var editor_%(name)s = CodeMirror.fromTextArea('id_%(name)s', {
            path: "%(CODEEDITOR_MEDIA_URL)sjs/",
            height: "%(height)s",
            autoMatchParens:  true,
            parserfile: %(parserFiles)s,
            stylesheet: %(stylesheets)s,
            lineNumbers: true,
            indentUnit: 4,
            tabMode: "shift"
        });
    };
</script>
""" 

    SYNTAXES  = {
              'css':   (('parsecss.js',),('csscolors.css',)),
              'html':  (("parsexml.js", "parsecss.js", "tokenizejavascript.js", "parsejavascript.js", "parsehtmlmixed.js"), ('xmlcolors.css','jscolors.css','csscolors.css',)),
              'js':    (("parsejavascript.js","tokenizejavascript.js"), ('jscolors.css',)),
              'dummy': (("parsedummy.js",), ('dummy.css',))
             }

    editor_attrs = {
                    'CODEEDITOR_MEDIA_URL': urljoin( settings.MEDIA_URL , 'templatesadmin/codemirror/' ),
                    'syntax': 'html',
                    'indentUnit': '4',
                    'autoMatchParens': 'True',  
                    'lineNumbers': 'True',
                    'tabMode': 'shift',
                    'width':   '240px',
                    'height':  '300px'
                }

    def __init__(self, attrs=None):
        if attrs:
            self.editor_attrs.update(attrs)
        
        super(CodeMirrorEditor, self).__init__({'rows': '10','cols': '40'})

    def render(self, name, value, attrs=None):
        # Build textarea first
        if value is None: value = ''
        text_attrs    = self.build_attrs( attrs , name=name )
        textarea_html =  u'<textarea%s>%s</textarea>' % (flatatt(text_attrs), conditional_escape(force_unicode(value)))

        # Build the codemirror widget
        (parserFile,stylesheets) = self.syntax;
        codeeditor_html = self.CODEEDITOR_JS % dict(name=name , parserFiles=parserFile, stylesheets=stylesheets, **self.editor_attrs )

        return mark_safe( '\n'.join([textarea_html , codeeditor_html ]) )


    def _syntax(self):
        """
            Given a regular language, return the appropriate files
            (parserFiles + stylesheets ) in a js-dict-friendly format (remove u'str' formts)
        """
        syntax = self.editor_attrs['syntax']
        if syntax not in self.SYNTAXES:
            syntax = u'dummy'

        codemedia_url = self.editor_attrs['CODEEDITOR_MEDIA_URL']
        parserfiles = unicode([str(conditional_escape(urljoin(codemedia_url, "js/%s" % f))) for f in self.SYNTAXES[syntax][0] ])
        stylesheets = unicode([str(conditional_escape(urljoin(codemedia_url, "css/%s" % f))) for f in self.SYNTAXES[syntax][1] ])

        return parserfiles , stylesheets

    def _media(self):
        return forms.Media( js=( urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'] , 'js/codemirror.js') ,),
                            css={ 'all': (urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'] , 'css/codemirror.css'), )})

    syntax = property(_syntax)
    media  = property(_media)
