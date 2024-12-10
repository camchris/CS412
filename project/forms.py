from django import forms
from .models import Profile, JobPost, MediaPost

class CreateNewProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    address = forms.CharField(label="Address", required=True)
    email_address = forms.CharField(label="Email Address", required=True)
    date_of_birth = forms.DateField(label="Birth Date", required=True)
    profile_image_url = forms.CharField(label="Profile Image URL", required=True)

    class Meta:
        '''associate this form with the Profile model; select fields.'''
        model = Profile
        fields = ['first_name', 'last_name', 'address', 'email_address', 'date_of_birth', 'profile_image_url', ]  


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


class CreateJobPostForm(forms.ModelForm):
    '''A form to create a JobPost in the database.'''
    description = forms.CharField(label="Description", required=True)
    pay = forms.CharField(label="Pay", required=True)
    location = forms.CharField(label="Location", required=True)
    instrument = forms.ModelChoiceField(
        label="Instrument", 
        queryset=None,  # To be set dynamically in the view
        required=True
    )

    class Meta:
        '''Associate this form with the JobPost model and select fields.'''
        model = JobPost
        fields = ['description', 'pay', 'location', 'instrument']

class CreateMediaPostForm(forms.ModelForm):
    '''A form to create a MediaPost in the database.'''
    message = forms.CharField(label="Message", required=True)

    class Meta:
        '''Associate this form with the JobPost model and select fields.'''
        model = MediaPost
        fields = ['message']

