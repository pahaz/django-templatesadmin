from django.db import models
from django.core.exceptions import SuspiciousOperation

class FTemplate(models.Model):
    """
        Faking a model to use templatesadmin in
        admin site (without other hacks). I hack here
        to avoid the user to hack forward. 

        The name FTemplate avoid ugly-url (FakedTemplateModel)
    """
    class Meta:
        verbose_name , verbose_name_plural = "Template" , "Templates"
        managed = False

    def save(self, *args, **kwargs):
        raise SuspiciousOperation("TemplateAdmin model is faked. Sorry to disappoint you...")

    def delete(self, *args, **kwargs):
        raise SuspiciousOperation("TemplateAdmin model is faked. Sorry to disappoint you...")
