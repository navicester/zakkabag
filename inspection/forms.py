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

class DailyInspectionForm(forms.ModelForm):
    '''
    impact = forms.ModelMultipleChoiceField(
            queryset = OfficeInspection.objects.all(),
            widget = forms.SelectMultiple(),
            #widget=forms.CheckboxSelectMultiple(),
            initial = [OfficeInspection.objects.all()[0]],
            #data = [OfficeInspection.objects.all()[0]],
            required=False
            )
    '''

    
    impact = forms.MultipleChoiceField(
            choices = lambda: (item for item in DailyInspection.daily_insepction_impact),
            widget = forms.SelectMultiple(),
            #widget=forms.CheckboxSelectMultiple(),
            initial = ['environment'],
            #initial= lambda: [item for item in DailyInspection.daily_insepction_impact if item],
            required=True
            )
    

    def __init__(self, *args, **kwargs):
        '''
        impact_selcted = None
        try:
            impact_selcted = kwargs.pop('selected')
        except:
            pass
        '''

        super(DailyInspectionForm, self).__init__(*args, **kwargs)

        '''
        self.fields['impact'] = forms.MultipleChoiceField(
            choices= DailyInspection.daily_insepction_impact,
            widget = forms.SelectMultiple,
            #initial = [impact_selcted],
            initial = ['people'],
            required=False
            )
        '''

    def clear_image_after_clear(self):
        if self.data.get('image_after-clear'):
            return "on"
        return None

    def clear_image_before_clear(self):
        if self.data.get('image_before-clear'):
            return "on"
        return None

    class Meta:
        model = DailyInspection

        exclude = [
            'timestamp',
            'updated',
        ]
        


    # ModelChoiceField

    '''
    def clean_plug(self):
        return self.data.get('plug')
    '''
