from django import forms

from colourman.models import Colourman, Unacceptable, PrintingLog
from jobs.models import Job
from labels.models import Label


class SearchForm(forms.Form):
    search_term = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-start-0 ps-0',
                'placeholder': 'Search by name or clock number',
            }
        ),
    )


class AddColourmanForm(forms.ModelForm):
    class Meta:
        model=Colourman
        fields='__all__'
        widgets={
            'name': forms.TextInput(attrs={'placeholder': 'Name of the employee'}),
            'clock_number': forms.TextInput(attrs={'placeholder': 'Enter his/her clock number'}),
            'shift': forms.TextInput(attrs={'placeholder': 'Enter his/her shift'}),}
        error_messages={
            'name': {
                'required': 'Please enter employee name',
            },
            'clock_number': {
                'required': 'Please enter his/her clock number',
            },
            'shift': {
                'required': 'Please enter his/her shift',
            }
        }


class AddUnacceptableColourmanForm(forms.ModelForm):
    class Meta:
        model = Unacceptable
        fields='__all__'
        exclude=['colourman','created_at','updated_at']
        widgets={
            'reason': forms.Textarea(attrs={'placeholder': 'Reason for unacceptable'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Insert comment if need'}),
        }
        error_messages={
            'reason': {'required': 'Reason for unacceptable'},
        }
        labels={
            'reason': '',
            'comment': '',
        }


class AddPrintOrUsageOfLabelForm(forms.ModelForm):
    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter job code'}),
                           label="Job Code")
    class Meta:
        model = PrintingLog
        fields = '__all__'
        exclude = ['usage_date']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        code_id = self.data.get('code') or self.initial.get('code')
        the_job = Job.objects.filter(job_code=code_id).first()

        if code_id:
            self.fields['label'].queryset = the_job.labels.all()
            self.fields['label'].widget.attrs.pop('disabled', None)

        else:
            self.fields['label'].queryset = Label.objects.none()
            self.fields['label'].disabled = True
            setattr(self.fields['label'], 'empty_label', 'Please enter job code first')

    def clean_code(self):

        code_text = self.cleaned_data.get('code')
        try:

            job = Job.objects.get(job_code=code_text)
            return job
        except Job.DoesNotExist:
            raise forms.ValidationError(f"Job with code '{code_text}' does not exist.")
