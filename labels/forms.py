from django import forms
from django.forms import formset_factory

from labels.models import Label, LabelSize, LabelType


class LabelBaseForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = '__all__'
        widgets = {'label_types': forms.CheckboxSelectMultiple,
                   'bar_code': forms.TextInput(attrs={'placeholder': 'Add barcode only if it is a preprinted label type'}),}

    def clean(self):
        cleaned_data = super().clean()
        bar_code = cleaned_data.get('bar_code')
        label_types = cleaned_data.get('label_types')
        if bar_code and label_types:
            for l in label_types:
                if l and not l.is_preprinted:
                    self.add_error('bar_code', "You cannot add a barcode for a type that is not preprinted!")
        return cleaned_data



class SearchForm(forms.Form):
    search_term = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-start-0 ps-0',
                'placeholder': 'Search by job code or description',
            }
        ),
    )


class CreateLabelForm(LabelBaseForm):
    pass

class LabelFormSet(formset_factory(LabelBaseForm)):
    pass

class EditLabelForm(LabelBaseForm):
    pass

class DeleteLabelForm(LabelBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].disabled = True


class LabelSizeForm(forms.ModelForm):
    class Meta:
        model = LabelSize
        fields = '__all__'


class LabelTypeForm(forms.ModelForm):
    class Meta:
        model = LabelType
        fields = '__all__'
        widgets = {'sizes': forms.CheckboxSelectMultiple}
