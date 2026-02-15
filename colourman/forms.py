from django import forms


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