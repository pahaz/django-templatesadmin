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

        http://codemirror.net/doc/manual.html#config

        Ctrl-F / Cmd-F
            Start searching
        Ctrl-G / Cmd-G
            Find next
        Shift-Ctrl-G / Shift-Cmd-G
            Find previous
        Shift-Ctrl-F / Cmd-Option-F
            Replace
        Shift-Ctrl-R / Shift-Cmd-Option-F
            Replace all
        Ctrl-q
            Fold a block

    """

    CODEEDITOR_JS = """
<style>

    .CodeMirror {border-top: 1px solid black; border-bottom: 1px solid black;}
    .activeline {background: #e8f2ff !important;}

    span.CodeMirror-matchhighlight { background: #e9e9e9 }
    .CodeMirror-focused span.CodeMirror-matchhighlight { background: #e7e4ff; !important }

</style>
<script type="text/javascript">

    // for detect extension
    function get_extension() {
        var z = window.location.href.toString().split(window.location.host)[1].replace(/^\\+|\/+$/g,'').split('.');
        var extend = z[z.length-1];
        return extend;
    }
    function get_syntax_mode(ext, def) {
        var exts = {
            'html': 'django',
            'js': 'javascript',
            'css': 'css',
        };
        if (!def) {
            def = 'htmlmixed';
        }

        var use = exts[ext];
        if (use) return use;
        else return def;
    }

    function changeMode(editor, mdoe) {
       editor.setOption("mode", mdoe);
       CodeMirror.autoLoadMode(editor, mdoe);
    }

    function getSelectedRange(editor) {
        return { from: editor.getCursor(true), to: editor.getCursor(false) };
    }

    function autoFormatSelection(editor) {
        var range = getSelectedRange();
        editor.autoFormatRange(range.from, range.to);
    }

    function commentSelection(editor, isComment) {
        var range = getSelectedRange();
        editor.commentRange(isComment, range.from, range.to);
    }

    window.onload = function(e){

        var foldFunc_html = CodeMirror.newFoldFunction(CodeMirror.tagRangeFinder);
        var foldFunc = CodeMirror.newFoldFunction(CodeMirror.braceRangeFinder);

        CodeMirror.modeURL = "%(CODEEDITOR_MEDIA_URL)smode/%%N/%%N.js";
        CodeMirror.commands.autocomplete = function(cm) {
            CodeMirror.simpleHint(cm, CodeMirror.javascriptHint);
        }

        var editor_%(name)s = CodeMirror.fromTextArea(document.getElementById('id_%(name)s'), {

            indentUnit: 4,
            matchBrackets: true,
            lineNumbers: true,
            autoCloseBrackets: true,
            tabMode: "shift",
            onGutterClick: function(cm, n) { // FOR BREACKPINTS
                var info = cm.lineInfo(n);

                if (info.markerText)
                    cm.clearMarker(n);
                else
                    cm.setMarker(n, "<span style='color: #900'>!</span> %%N%%");

                 foldFunc(cm, cm.getCursor().line);
                 foldFunc_html(cm, cm.getCursor().line);

            },
            lineWrapping: true,
            styleActiveLine: true,
              extraKeys: {
                "Ctrl-Q": function(cm){
                     foldFunc(cm, cm.getCursor().line);
                     foldFunc_html(cm, cm.getCursor().line);
                },
                "Ctrl-H": function(cm){
                    alert("        Ctrl-F / Cmd-F \\n             Start searching \\n         Ctrl-G / Cmd-G \\n             Find next \\n         Shift-Ctrl-G / Shift-Cmd-G \\n             Find previous \\n         Shift-Ctrl-F / Cmd-Option-F \\n             Replace \\n         Shift-Ctrl-R / Shift-Cmd-Option-F \\n             Replace all \\n         Ctrl-q \\n             Fold a block");
                },
                "Ctrl-Space": "autocomplete"
            },

        });

        window.editor_%(name)s = editor_%(name)s; // export;

        var syntax_mode = get_syntax_mode(get_extension(), "%(syntax)s");
        changeMode(editor_%(name)s, syntax_mode);
        console.log('for "editor_%(name)s" use "' + syntax_mode + '" mode');
    };
</script>
"""

    editor_attrs = {
                    'CODEEDITOR_MEDIA_URL': urljoin( settings.STATIC_URL , 'templatesadmin/codemirror/' ),
                    'syntax': "htmlmixed",
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
        codeeditor_html = self.CODEEDITOR_JS % dict(name=name , **self.editor_attrs)

        return mark_safe( '\n'.join([textarea_html , codeeditor_html ]) )

    def _media(self):
        return forms.Media(
            js=(
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'lib/codemirror.js'),
                # urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/dialog/dialog.js'), # Disabled because not working in search.js (auto-closed on lost focus)
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/search/searchcursor.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/search/search.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/search/match-highlighter.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/fold/foldcode.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/mode/loadmode.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/edit/matchbrackets.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/edit/closebrackets.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/edit/matchtags.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/selection/active-line.js'),


                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'addon/mode/overlay.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'mode/xml/xml.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'mode/htmlmixed/htmlmixed.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'mode/django/django.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'mode/javascript/javascript.js'),
                urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'], 'mode/css/css.js'),
            ),
            css={
                'all': (
                    urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'] , 'lib/codemirror.css'),
                    urljoin(self.editor_attrs['CODEEDITOR_MEDIA_URL'] , 'addon/dialog/dialog.css'),
                )
            }
        )

    media = property(_media)
