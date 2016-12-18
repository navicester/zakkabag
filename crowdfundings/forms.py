from django import forms
from .models import Crowdfunding

class CrowdfundingCreateForm(forms.ModelForm):
	class Meta:
		model = Crowdfunding

		fields = [
			'title',
		# 	'description',
		# 	'price',
		# 	'active',
		# 	'categories',
		# 	'default'
		]

# class ProductImageForm(forms.ModelForm):
# 	class Meta:
# 		model = ProductImage
# 		fields = [
# 			'image',
# 			# 'product'
# 		]

# 	def clean_image(self):
# 		if self.cleaned_data.get("image") != None:
# 			return self.cleaned_data.get("image")
# 		elif self.data.get("image") == None:	
# 			raise forms.ValidationError("image can't be empty.")
# 		else:
# 			self.cleaned_data['image'] = self.data.get("image")
# 			return self.data.get("image")

# 	def is_valid(self):
# 		if self.clean_image != None:
# 			return True
# 		return False		