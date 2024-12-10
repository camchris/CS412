from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    '''Profiles for final project.'''

    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    address = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    date_of_birth = models.DateField()
    profile_image_url = models.TextField(blank=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def get_friends(self):
        '''Return all of the friends of this profile.'''
        friend1_profiles = Profile.objects.filter(profile2__profile1=self)
        friend2_profiles = Profile.objects.filter(profile1__profile2=self)

        return (friend1_profiles | friend2_profiles).distinct()
    
    def get_friend_suggestions(self):
        '''Suggest friends to profile'''
        current_friends = self.get_friends()
        suggestions = set() 

        for friend in current_friends:
            potential_friends = friend.get_friends()
            for potential_friend in potential_friends:
                if potential_friend != self and potential_friend not in current_friends and potential_friend not in suggestions:
                    suggestions.add(potential_friend)

        if len(suggestions) == 0:
            all_profiles = set(Profile.objects.all())
            suggestions = all_profiles - {self} - set(current_friends)
        return list(suggestions)
    
    def get_instruments(self):
        '''Return all of the instruments of this profile.'''
        instruments = UserInstrument.objects.filter(profile=self)
        return instruments
    
    def get_instrument_suggestions(self):
        '''Return all of the instrument suggestions of this profile.'''
        current_instruments = UserInstrument.objects.filter(profile=self).values_list('instrument', flat=True)
        suggestions = Instrument.objects.exclude(id__in=current_instruments)
        return suggestions
    
    def get_mediaposts(self):
        '''Return all of the status messages of this profile.'''
        posts = MediaPost.objects.filter(profile=self)
        return posts
    
    def get_news_feed(self):
        profile_sm = self.get_mediaposts()
        friends = self.get_friends()
        newsfeed = set(profile_sm) 
        for f in friends:
            for m in f.get_mediaposts():
                newsfeed.add(m)
        return list(newsfeed)
    
    def add_friend(self, other):
        '''Add a friend to this profile.'''
        if other in self.get_friends() or self == other:
            return "Cannot add friend."
        else:
            Friend.objects.create(profile1=self, profile2=other)
            return "Friend added successfully."
        
    def add_instrument(self, other):
        '''Add an instrument to this profile.'''
        if other in self.get_instruments():
            return "Cannot add instrument."
        else:
            UserInstrument.objects.create(profile=self, instrument=other)
            return "Instrument added successfully."
        
    def get_jobposts(self):
        '''Return all of the jobposts of this profile.'''
        jobposts = JobPost.objects.filter(profile=self)
        return jobposts
    
    def get_mediaposts(self):
        '''Return all of the mediaposts of this profile.'''
        mediaposts = MediaPost.objects.filter(profile=self)
        return mediaposts
        

    def get_absolute_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return reverse('show_profile', kwargs={'pk': self.pk})
        
    
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
    '''Instrument class for final project'''

    name = models.TextField(blank=False)
    image_url = models.TextField(blank=False)
    family = models.TextField(blank=False)

    def get_profiles(self):
        '''Return all of the profiles that play this instrument.'''
        profiles = UserInstrument.objects.filter(instrument=self)
        return profiles

    def __str__(self):
        '''Return a string representation of this Instrument object.'''
        return f'{self.name}'

class UserInstrument(models.Model):
    '''Instrument Relationship class for final project'''

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile')
    instrument = models.ForeignKey("Instrument", on_delete=models.CASCADE, related_name='instrument')
    time_played = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this relationship.'''
        return f'{self.profile.first_name}, {self.instrument.name}'

class MediaPost(models.Model):
    '''MediaPost for final project'''
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
    '''Image class for final project.'''
    image_file = models.ImageField(blank=True)
    media_post = models.ForeignKey("MediaPost", on_delete=models.CASCADE, related_name='images')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Image object.'''
        return f'{self.timestamp}: {self.media_post.message}'
    
class Video(models.Model):
    '''Video class for final project.'''
    video_file = models.FileField(upload_to='videos/', blank=True)
    media_post = models.ForeignKey("MediaPost", on_delete=models.CASCADE, related_name='videos')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Video object.'''
        return f'{self.timestamp}: {self.media_post.message}'
    

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

