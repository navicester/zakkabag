from django.db import models
 
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.db.models.signals import post_delete, post_save, pre_save
from .utils import file_cleanup, file_cleanup2, save_raw_instance
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils import timezone

# Create your models here.

RESULT_OPTION = (
    ('yes', 'Yes'),
    ('no', 'No'),
)

# inspection/office/
def image_upload_to(instance, filename):
    title, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(instance.timestamp, slugify(title), file_extension)
    return "inspection/%s/%s" %(instance.location, new_filename)

class OfficeInspection(models.Model):
	plug = models.CharField(_('plug'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
	power = models.CharField(_('power'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
	comments = models.TextField(blank=True, null=True)
	location = models.CharField(max_length=120, blank=False, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	image = models.ImageField(upload_to=image_upload_to, blank=True, null=True)

	def __unicode__(self): 
		return "Office " + self.location

	def get_absolute_url(self):
		return reverse("OfficeInspection_detail", kwargs={"pk": self.id })



def image_upload_to_dailyinspection(instance, filename):
    title, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(instance.created.strftime('%Y-%m-%d-%H-%M-%S'), slugify(title), file_extension)
    return "dailyinspection/%s/%s" %(instance.cateory, new_filename)

class DailyInspection(models.Model):
    daily_insepction_category = (
        ('people', _('People')),
        ('device', _('Device')),
        ('machine', _('Machine')),
        ('method', _('Method')),
        ('environment', _('Environment')),
    )

    # index can only be 1 char, see SelectMultiple:render & Select(Widget):render_options / selected_choices = set(force_text(v) for v in selected_choices) ==> bug ? set([force_text(v)]
    daily_insepction_impact = (
        ('1', 'People'),
        ('2', 'Device'),
        ('3', 'Machine'),
        ('4', 'Method'),
        ('5', 'Environment'),
    )

    daily_insepction_correction_status = (
        ('completed', _('Completed')),
        ('uncompleted', _('Uncompleted')),
    )

    daily_insepction_warehouse = (
        ('3', '3#'),
        ('5', '5#'),
    )

    cateory = models.CharField(_('cateory'), max_length=30, choices = daily_insepction_category, blank=False, default = 'people')
    item = models.CharField(_('item'), max_length=30, blank=False)
    impact = models.CharField(_('impact'), max_length=30, blank=False)
    correct = models.TextField(_('correct'), max_length=30, blank=False)
    correct_status = models.CharField(_('correct status'), max_length=30, choices = daily_insepction_correction_status, blank=False, default = 'Uncompleted')
    owner = models.CharField(_('owner'), max_length=30, blank=False)
    due_date = models.DateField(_('due date'), auto_now_add=False, auto_now=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    image_before = models.ImageField(_('image before'), upload_to=image_upload_to_dailyinspection, blank=True, null=True)
    image_after = models.ImageField(_('image after'), upload_to=image_upload_to_dailyinspection, blank=True, null=True)
    warehouse = models.CharField(_('warehouse'), max_length=30, choices = daily_insepction_warehouse, blank=False, default = '3#')
    
    def __unicode__(self): 
        return "daily inspection " + self.item

    def get_absolute_url(self):
        return reverse("dailyinspection_detail", kwargs={"pk": self.id })    

    def get_image_url_before(self):
        img = self.image_before
        if img:
            return img.url
        return img     

    def get_image_url_after(self):
        img = self.image_after
        if img:
            return img.url
        return img 

    def get_html_due_date(self):
        if self.due_date is not None:
            overdue = ''
            if self.due_date <= datetime.datetime.now().date() - datetime.timedelta(days=1): # should be 0
                overdue = 'overdue'
            html_text = "<span class='due_date %s'>%s</span>" %(overdue, self.due_date)
        else:
            html_text = "<span class='due_date'></span>"
        return mark_safe(html_text)

post_delete.connect(file_cleanup, sender=DailyInspection, dispatch_uid="DailyInspection.file_cleanup")
post_save.connect(file_cleanup2, sender=DailyInspection, dispatch_uid="DailyInspection.file_cleanup2")
pre_save.connect(save_raw_instance, sender=DailyInspection)