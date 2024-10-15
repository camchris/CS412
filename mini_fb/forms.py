from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email_address = forms.CharField(label="Email Address", required=True)
    profile_image_url = forms.CharField(label="Profile Image URL", required=True)

    class Meta:
        '''associate this form with the Profile model; select fields.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url', ]  

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a StatusMessage to the database.'''
    # timestamp & profile needed
    #message = forms.CharField(label="Message", required=True)

    class Meta:
        '''associate this form with the StatusMessage model; select fields.'''
        model = StatusMessage
        fields = ['message', ]