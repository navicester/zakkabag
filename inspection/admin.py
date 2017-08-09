from django.contrib import admin
from .models import OfficeInspection

# Register your models here.
class OfficeInspectionAdmin(admin.ModelAdmin):
	list_display = ["location", "plug",'timestamp']
	class Meta:
		model = OfficeInspection



admin.site.register(OfficeInspection, OfficeInspectionAdmin)