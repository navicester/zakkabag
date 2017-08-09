from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

# Create your models here.

RESULT_OPTION = (
    ('yes', 'Yes'),
    ('no', 'No'),
)

class OfficeInspection(models.Model):
	plug = models.CharField(_('plug'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
	location = models.CharField(max_length=120, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self): 
		return "Office " + self.location

	def get_absolute_url(self):
		return reverse("OfficeInspection_detail", kwargs={"pk": self.id })			