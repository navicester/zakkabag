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
    correct_status = models.CharField(_('correct status'), max_length=30, choices = daily_insepction_correction_status, blank=False, default = 'uncompleted')
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


class forklift(models.Model):
    """docstring for forklift"""

    internal_car_number = models.CharField(_('Inner Car Number'), max_length=30, blank=False)
    internal_plate_number = models.CharField(_('Inner Plate Number'), max_length=30, blank=False)
    model = models.CharField(_('Forklift Model'), max_length=30, blank=False)
    sn = models.CharField(_('SN'), max_length=30, blank=False)
    category = models.CharField(_('Forklift Category'), max_length=30, blank=False)
    manufacturer = models.CharField(_('Manufacturer'), max_length=30, blank=False)
    tip_height = models.CharField(_('Tip Height'), max_length=30, blank=False)
    carrying_capacity = models.CharField(_('Carrying Capacity'), max_length=30, blank=False)
    self_weight = models.CharField(_('Self Weight'), max_length=30, blank=False)
    turning_radius = models.CharField(_('Turning Radius'), max_length=30, blank=False)
    front_tyre_size = models.CharField(_('Front Tyre Size'), max_length=30, blank=False)
    back_tyre_size = models.CharField(_('Back Tyre Size'), max_length=30, blank=False)
    width = models.CharField(_('Forklift Width'), max_length=30, blank=False)
    length = models.CharField(_('Forklift Length'), max_length=30, blank=False)
    fork_length = models.CharField(_('Fork Length'), max_length=30, blank=False)
    maximum_velocity = models.CharField(_('Maximum Velocity'), max_length=30, blank=False)

    def __init__(self, arg):
        super(forklift, self).__init__()
        self.arg = arg

    def __unicode__(self): 
        return _("forklift") + self.internal_car_number

class forklift_image(models.Model):
    forklift = models.ForeignKey(forklift)
    image = models.ImageField(_('image'), upload_to='inspection/forklift', blank=True, null=True)

class forklift_maint(models.Model):
    """docstring for forklift_maint"""
    clean_forklift = models.CharField(_('clean forklift'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    clean_and_lubricate_chain = models.CharField(_('clean and lubricate chain'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    lubricate_gateshelf_and_lean_cylinder_bearing = models.CharField(_('lubricate gateshelf and lean cylinder bearing'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    lubricate_sideswayfork_and_check_work_status = models.CharField(_('lubricate sideswayfork and check work status'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    fastening_tyre_nut = models.CharField(_('fastening tyre nut'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_tyre_status = models.CharField(_('check tyre status'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_gear_oil_level_and_leak = models.CharField(_('check gear oil level and leak'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_hydraulic_oil_level = models.CharField(_('clean forklift'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    clean_all_motor_and_accessories = models.CharField(_('clean all motor and accessories'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_and_clean_motor_cooling_fan = models.CharField(_('check and clean motor cooling fan'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_all_cable_and_connection_status = models.CharField(_('check all cable and connection status'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_battery_electrolyte_liquidometer_ratio = models.CharField(_('check battery electrolyte liquidometer ratio'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_charger_status = models.CharField(_('check charger status'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_pipeline_fastening_and_leak = models.CharField(_('check pipeline fastening and leak'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_pallet_fork_and_pin_lock = models.CharField(_('check pallet fork and pin lock'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_lubricate_pedal_and_control_linkage = models.CharField(_('check lubricate pedal and control linkage'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_braking_device = models.CharField(_('check braking device'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_all_motor_carbon_brush = models.CharField(_('check all motor carbon brush'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_overhead_guard_and_counter_weight = models.CharField(_('check overhead guard and counter weight'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_steering_axle_and_drive_axle = models.CharField(_('check steering axle and drive axle'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_gateshelf_and_chain = models.CharField(_('check gateshelf and chain'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_hub_bearing = models.CharField(_('check hub bearing'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_steering_axle_bearing = models.CharField(_('check steering axle bearing'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    check_gateshlf_bearing = models.CharField(_('check gateshlf bearing'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    change_gear_oil = models.CharField(_('change gear oil'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    change_oil_suction_filter = models.CharField(_('change oil suction filter'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    change_ventilate_filter = models.CharField(_('change ventilate filter'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    change_hydraulic_oil = models.CharField(_('change hydraulic oil'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self): 
        return _("forklift") + self.internal_car_number

    def __init__(self, arg):
        super(forklift_maint, self).__init__()
        self.arg = arg


class forklift_repair(models.Model):
    damage_reason = models.CharField(_('Damage Reason'), max_length=30, blank=True)
    accessories_name = models.CharField(_('Accessories Name'), max_length=30, blank=True)
    accessories_num = models.DecimalField(_('Accessories Number'), decimal_places=0, max_digits=20, blank=True)
    description = models.TextField(_('Description'), max_length=30, blank=False)  
    repaired = models.CharField(_('Repaired'), max_length=30, choices = RESULT_OPTION, blank=True, default = 'no')  
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
class forklift_annual_inspection(models.Model):
    date = models.DateField(_('Date'), auto_now_add=False, auto_now=False)
    next_date = models.DateField(_('Next Inspection Date'), auto_now_add=False, auto_now=False)

class forklift_annual_inspection_image(models.Model):
    forklift = models.ForeignKey(forklift_annual_inspection)
    image = models.ImageField(_('image'), upload_to='inspection/forklift_annual_inspection', blank=True, null=True)

class shelf(models.Model):
    type = models.CharField(_('Damage Reason'), max_length=30, blank=True)    
    warehouse = models.CharField(_('Warehouse'), max_length=30, blank=True)
    compartment = models.CharField(_('Compartment'), max_length=30, blank=True)
    warehouse_channel = models.CharField(_('Warehouse Channel'), max_length=30, blank=True)
    group = models.CharField(_('group'), max_length=30, blank=True)
    number = models.CharField(_('number'), max_length=30, blank=True)    
    is_gradient_measurement_mandatory = models.BooleanField(_('Gradient Measurement Mandatory'), blank=True)

class shelf_inspection_record(models.Model):
    shelf = models.ForeignKey(shelf)
    use_condition = models.CharField(_('Use Condition'), max_length=30, blank=True) 
    is_locked = models.BooleanField(_('Locked'), blank=True)
    check_person = models.CharField(_('Check Person'), max_length=30, blank=True)
    gradient = models.DecimalField(_('Gradient'), decimal_places=1, max_digits=20, blank=True)
    comments = models.TextField(_('Comments'), max_length=30, blank=False)
