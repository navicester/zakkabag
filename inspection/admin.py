from django.contrib import admin
from .models import OfficeInspection, DailyInspection
from .forms import DailyInspectionForm

# Register your models here.
class OfficeInspectionAdmin(admin.ModelAdmin):
	list_display = ["location", "plug",'timestamp']
	class Meta:
		model = OfficeInspection

class DailyInspectionAdmin(admin.ModelAdmin):
	list_display = ["cateory", "correct_status",'owner']
	form = DailyInspectionForm
	
	class Meta:
		model = DailyInspection
		



admin.site.register(DailyInspection, DailyInspectionAdmin)

admin.site.register(OfficeInspection, OfficeInspectionAdmin)