from django import forms
from .models import OfficeInspection


RESULT_OPTION = (
    ('yes', 'Yes'),
    ('no', 'No'),
)

class OfficeInspectionForm(forms.ModelForm):
    class Meta:
        model = OfficeInspection

        fields = [
            'plug',
            'location',
        ]     

               
    plug = forms.MultipleChoiceField(
            choices=RESULT_OPTION,
            widget = forms.RadioSelect,
            )

    # ModelChoiceField
    