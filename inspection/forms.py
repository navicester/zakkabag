from django import forms
from .models import OfficeInspection, DailyInspection, shelf_inspection_record
from django.utils.translation import ugettext_lazy as _
from django.forms import BaseFormSet,BaseModelFormSet, formset_factory
from django.forms.models import modelformset_factory

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
    
    
    impact = forms.MultipleChoiceField(
            choices = lambda: (item for item in DailyInspection.daily_insepction_impact),
            widget = forms.SelectMultiple(),
            #widget=forms.CheckboxSelectMultiple(),
            initial = ['environment'],
            #initial= lambda: [item for item in DailyInspection.daily_insepction_impact if item],
            required=True
            )

    def __init__(self, *args, **kwargs):
        super(DailyInspectionForm, self).__init__(*args, **kwargs)

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

class InspectionFilterForm(forms.Form):
    q = forms.CharField(label='Search', required=False)
    '''
    category_id = forms.ModelMultipleChoiceField(
        label='Category',
        queryset=Category.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=False)
    '''

    category = forms.MultipleChoiceField(
            label=_('Category'),
            choices = DailyInspection.daily_insepction_category,
            #widget = forms.SelectMultiple(),
            widget=forms.CheckboxSelectMultiple(),
            initial = None,
            required=False
            )    

    rectification_status = forms.ChoiceField(
            label=_('Rectification Status'),
            choices = DailyInspection.daily_insepction_correction_status,
            widget=forms.RadioSelect(),
            required=False
            )   
    #owner = forms.CharField(label='Owner',required=False)
    owner = forms.ChoiceField(
            label=_('Owner'),
            choices = set((dailyinspection.owner,dailyinspection.owner) for dailyinspection in DailyInspection.objects.all()),
            widget=forms.RadioSelect(),
            initial = None,
            required=False
            )    

class shelf_inspection_recordForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(shelf_inspection_recordForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.instance1 = instance
            print 'self.instance in init >>>>>>>>>'
            print self.instance
            #self.fields['shelf'].widget.attrs['readonly'] = True
            self.fields['shelf'].widget.attrs['disabled'] = True

    def clean(self):

        self.cleaned_data['shelf'] = self.clean_shelf()        
        #print self.cleaned_data
        return self.cleaned_data

    def clean_shelf(self):
        instance = getattr(self, 'instance', None)
        
        if instance and instance.id:
            return instance.shelf
        elif self.cleaned_data.get('shelf', None):
            return self.cleaned_data['shelf']
        else:
            id = self.cleaned_data.get('id', None)
            if id:
                try:
                    shelf_inspection_record_instance = shelf_inspection_record.objects.get(pk=id)
                    return shelf_inspection_record_instance.shelf
                except:
                    return None
            else:
                return None


    class Meta:
        model = shelf_inspection_record

        exclude = [
            'shelf_inspection',
            'comments',
            'check_person'
        ]

        # workaround, not sure whether this function is already exist
        disabled = [
            'shelf'
        ]

        hidden = [
            'id'
        ]


class shelf_inspection_recordModelFormSet(BaseModelFormSet):
    def is_valid(self):
        return super(shelf_inspection_recordModelFormSet, self).is_valid()

shelf_inspection_record_Formset = modelformset_factory(shelf_inspection_record, 
                                            form=shelf_inspection_recordForm, 
                                            formset=shelf_inspection_recordModelFormSet, 
                                            extra=0)