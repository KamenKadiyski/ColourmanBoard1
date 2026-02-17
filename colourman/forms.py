from django import forms

from colourman.models import Colourman, Unacceptable


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