from django import forms
from .models import Profile, Instrument

class EditProfileForm(forms.ModelForm):
    '''A form to update Profiles.'''

    address = forms.CharField(label="Address", required=True)
    email_address = forms.CharField(label="Email Address", required=True)
    profile_image_url = forms.CharField(label="Profile Image URL", required=True)
    date_of_birth = forms.DateField(label="Birth Date", required=True)

    class Meta:
        '''associate this form with the Profile model; select fields.'''
        model = Profile
        fields = ['address', 'email_address', 'profile_image_url', 'date_of_birth'] 