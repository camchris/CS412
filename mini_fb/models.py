from django.db import models
from django.urls import reverse

class Profile(models.Model):
    '''Profiles for mini_fb.'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    profile_image_url = models.TextField(blank=False)

    def get_status_messages(self):
        '''Return all of the status messages of this profile.'''
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    def get_absolute_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'
    

class StatusMessage(models.Model):
    '''StatusMessage for mini_fb.'''
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def get_images(self):
        '''get images for the status message'''
        return self.images.all()

    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.message}'
    
class Image(models.Model):
    '''Image class for mini_fb.'''
    image_file = models.ImageField(blank=True)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE, related_name='images')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.timestamp}'
