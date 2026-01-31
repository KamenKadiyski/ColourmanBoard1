from django import forms
from django.forms import formset_factory

from labels.models import Label, LabelSize, LabelType


class LabelBaseForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = '__all__'


class SearchForm(forms.Form):
    search_term = forms.CharField(label='Search', max_length=100)


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