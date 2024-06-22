from django import forms
from .models import Provider, Service, BusinessHours

# Constants for the time choices (e.g., 00:00 to 23:30 in 30-minute intervals)
TIME_CHOICES = [(f"{hour:02}:{minute:02}:00", f"{hour:02}:{minute:02}") for hour in range(24) for minute in (0, 30)]

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'email', 'phonenumber', 'address', 'city', 'postalcode', 'country']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Street, number'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'postalcode': forms.TextInput(attrs={'placeholder': 'Postal code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }

class ServiceForm(forms.ModelForm):
    DURATION_CHOICES = [
        (15*60, '15 minutes'),
        (30*60, '30 minutes'),
        (45*60, '45 minutes'),
        (60*60, '60 minutes'),
        (75*60, '75 minutes'),
        (90*60, '90 minutes'),
        (120*60, '120 minutes'),
    ]

    length = forms.ChoiceField(choices=DURATION_CHOICES, widget=forms.Select())
    class Meta:
        model = Service
        fields = ['name', 'description', 'length']

class BusinessHoursForm(forms.ModelForm):
    day_label = forms.CharField(widget=forms.HiddenInput(), required=False)
    open_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select)
    close_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select)

    class Meta:
        model = BusinessHours
        fields = ['day', 'open_time', 'close_time']
        widgets = {
            'day': forms.HiddenInput()
        }

BusinessHoursFormSet = forms.inlineformset_factory(
    Provider,
    BusinessHours,
    form=BusinessHoursForm,
    extra=7,
    can_delete=False,
)
