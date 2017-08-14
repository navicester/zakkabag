from django import forms
from .models import OfficeInspection, DailyInspection


RESULT_OPTION = (
    ('yes', 'Yes'),
    ('no', 'No'),
)

class OfficeInspectionForm(forms.ModelForm):
    class Meta:
        model = OfficeInspection

        exclude = [
            'timestamp',
            'updated',
            'image'
        ]
        

               
    #plug = forms.MultipleChoiceField(
    plug = forms.ChoiceField(
            choices=RESULT_OPTION,
            widget = forms.RadioSelect,
            )

    power = forms.ChoiceField(
            choices=RESULT_OPTION,
            widget = forms.RadioSelect,
            )
    # ModelChoiceField

    '''
    def clean_plug(self):
        return self.data.get('plug')
    '''

daily_insepction_impact = (
    ('people', 'People'),
    ('device', 'Device'),
    ('machine', 'Machine'),
    ('method', 'Method'),
    ('environment', 'Environment'),
)

class DailyInspectionForm(forms.ModelForm):
    class Meta:
        model = DailyInspection

        exclude = [
            'timestamp',
            'updated',
        ]
        

    impact = forms.MultipleChoiceField(
            choices=daily_insepction_impact,
            widget = forms.SelectMultiple,
            )

    # ModelChoiceField

    '''
    def clean_plug(self):
        return self.data.get('plug')
    '''
