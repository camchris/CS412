from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    '''Profiles for music_network.'''

    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    address = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    date_of_birth = models.DateField()
    profile_image_url = models.TextField(blank=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="temp1")
    
    def get_friends(self):
        '''Return all of the friends of this profile.'''
        friend1_profiles = Profile.objects.filter(profile2__profile1=self)
        friend2_profiles = Profile.objects.filter(profile1__profile2=self)

        return (friend1_profiles | friend2_profiles).distinct()
    
    def get_instruments(self):
        '''Return all of the instruments of this profile.'''
        instruments = UserInstrument.objects.filter(profile=self)
        return instruments
    
    def add_friend(self, other):
        '''Add a friend to this profile.'''
        if other in self.get_friends() or self == other:
            return "Cannot add friend."
        else:
            Friend.objects.create(profile1=self, profile2=other)
            return "Friend added successfully."
        
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'


class Friend(models.Model):
    '''Friend class for music_network.'''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}'
    
class Instrument(models.Model):
    '''Instrument class for music_network'''

    name = models.TextField(blank=False)
    image_url = models.TextField(blank=False)
    family = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this Instrument object.'''
        return f'{self.name}'

class UserInstrument(models.Model):
    '''Instrument Relationship class for music network'''

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile')
    instrument = models.ForeignKey("Instrument", on_delete=models.CASCADE, related_name='instrument')
    time_played = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this relationship.'''
        return f'{self.profile.first_name}, {self.instrument.name}'

class MediaPost(models.Model):
    '''MediaPost for music_network'''
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def get_images(self):
        '''get images for the media post'''
        return self.images.all()
    
    def get_videos(self):
        '''get videos for the media post'''
        return self.videos.all()

    def __str__(self):
        '''Return a string representation of this MediaPost object.'''
        return f'{self.message}'
    
class Image(models.Model):
    '''Image class for music_network.'''
    image_file = models.ImageField(blank=True)
    media_post = models.ForeignKey("MediaPost", on_delete=models.CASCADE, related_name='images')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Image object.'''
        return f'{self.timestamp}'
    
class Video(models.Model):
    '''Video class for music_network.'''
    video_file = models.FileField(upload_to='videos/', blank=True)
    media_post = models.ForeignKey("MediaPost", on_delete=models.CASCADE, related_name='videos')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Video object.'''
        return f'{self.timestamp}'
    

class JobPost(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    instrument = models.ForeignKey("Instrument", on_delete=models.CASCADE)
    pay =  models.TextField(blank=False)
    location =  models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this JobPost object.'''
        return f'{self.description}'

