from django import forms

from jobs.models import Job, Customer


class JobSearchForm(forms.Form):
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



class AddJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        labels = cleaned_data.get('labels')
        barcode = cleaned_data.get('barcode')

        if not labels:
            return cleaned_data


        has_preprinted = labels.filter(label_types__is_preprinted=True).exists()

        if has_preprinted:
            pass
        else:
            if not barcode:
                self.add_error('barcode', 'Please, enter barcode')

        return cleaned_data


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_code', 'description','customer','labels','barcode']
        widgets = {
            'job_code': forms.TextInput()
        }



class CustomerSearchForm(forms.Form):
    search_term = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-start-0 ps-0',
                'placeholder': 'Search by customer',
            }
        ),
    )

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


