===============
Templates Admin
===============

Templates Admin is a tiny, nifty application for your Django_ project to edit
your templates, that are stored on your disk, via an admin interface.

Originally this app was inspired by dbtemplates_.

.. _Django: http://www.djangoproject.com/
.. _dbtemplates: http://code.google.com/p/django-dbtemplates/

Installation:
=============

1. Put ``templatesadmin`` into your INSTALLED_APPS setting.

2. Create a group ``TemplateAdmins`` and put all users in there, who should been
   able to edit templates. You don't need to grant any permissions to that group.
   Just call it ``TemplateAdmins``.
   
   Admins don't need to belong this group. The group name is case-sensitive!

3. Make ``media/templatesadmin/`` available in your MEDIA_PATH.

4. Point your webbrowser to ``http://localhost/admin/templatesadmin/`` and start 
   editing.
   
Optional Settings:
==================

There are some settings that you can override in your ``settings.py``:

1. ``TEMPLATESADMIN_GROUP``: The name of your group of your TemplatesAdmin
   Users. 
   
   Default: ``TemplateAdmins``
   
2. ``TEMPLATESADMIN_VALID_FILE_EXTENSIONS``: A tuple of file-extensions (without
   the leading dot) that are editable by TemplatesAdmin.
   
   Default::
   
    TEMPLATESADMIN_VALID_FILE_EXTENSIONS = (
        'html', 
        'htm', 
        'txt', 
        'js',
        'css', 
        'backup'
    )

3. ``TEMPLATESADMIN_TEMPLATE_DIRS``: A tuple of directories you want your users
   to edit, instead of all templates.

   Default: All user-defined and application template-dirs.

4. ``TEMPLATEADMIN_USE_RICHEDITOR``: is deleted! Default use CodeMirror editor.

5. ``TEMPLATESADMIN_HIDE_READONLY``: A boolean to wether enable or disable
   displaying of read-only templates.
   
   Default: ``False``

6. ``TEMPLATESADMIN_EDITHOOKS``: A tuple of callables edithooks. Edithooks are
   a way to interact with changes made on a template. Think of a plugin system.

   There are four builtin edithooks:
   
   - ``dotbackupfiles.DotBackupFilesHook``: Creates a copy of the original file
     before overwriting, naming it ``<oldname>.backup``.
   - ``gitcommit.GitCommitHook``: Commits your templates after saving via git
     version control.
   - ``hgcommit.HgCommitHook``: Creates a `mercurial
     <http://www.selenic.com/mercurial/>`_ commit after saving.
   - ``svncommit.SvnCommitHook``: Commits your templates after saving
     via ``svn``.

   You can define your own edithooks, see above hooks as example. 
   
   Default::
   
    TEMPLATESADMIN_EDITHOOKS = (    
        'templatesadmin.edithooks.dotbackupfiles.DotBackupFilesHook',
    )
   

LICENSE:
========

This application is licensed under the ``Beerware License``.
See ``LICENSE`` for details.

Changelog:
==========

**v0.75 (2012-11-21)

* Django 1.5 ready.
* Change editor on Codemirror v 2.36: (http://codemirror.net/).
* Add cool addons for editor.
* Deleted: TemplateForm and RechTemplateForm.

**v0.65 (2010-05-19)**

* Django 1.2 ready
* Included Rich code editor (http://marijn.haverbeke.nl/codemirror/) with automatically
  syntax highlight.
* Refactored to a Admin application.
* Included a new CommitHook (``SvnCommitHook``)

**v0.6 (2009-09-08)**

* Published under a proper BSD license.
* The templates now inherits from the Django templates to provide a better
  look and feel.
* A lot of overall improvements from typo fixing to better permission handling.
  Thanks to peritus and rlaager.
  
**v0.5.5 (2009-02-13)**

* Documented that there is a edithook for mercurial repositories.
* Bugfix in GitCommitHook: Allow non-ascii characters.

**v0.5.4 (2009-02-13)**

* Fixed missing templatetags in pypi release.

**v0.5.3 (2009-02-03)**

* Edit-Views now have an optional argument "base_form" to overwrite the default form.
* Removed shorten-path functions. They didn't work under some conditions.
* List of templates in the admin overview are shorter.

**v0.5.2 (2008-12-12)**

* Added a edithook for dealing with mercurial repositories. Thank you v.oostveen! (Issue3_)
* Fixed handling of newline characters at the end of the file, which causes to 
  delete the last character. (Issue4_)

.. _Issue3: http://code.google.com/p/django-templatesadmin/issues/detail?id=3
.. _Issue4: http://code.google.com/p/django-templatesadmin/issues/detail?id=4
