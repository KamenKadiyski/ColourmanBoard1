from django import forms

from jobs.models import Job


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
                'placeholder': 'Search by customer or description',
            }
        ),
    )