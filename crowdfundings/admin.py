from django.contrib import admin

# Register your models here.
from .models import Crowdfunding

class CrowdfundingAdmin(admin.ModelAdmin):
	list_display = ['id', '__unicode__', ]

	class Meta:
		model = Crowdfunding

admin.site.register(Crowdfunding, CrowdfundingAdmin)
