from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    '''Profiles for mini_fb.'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.TextField(blank=False)
    profile_image_url = models.TextField(blank=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="temp")

    def get_status_messages(self):
        '''Return all of the status messages of this profile.'''
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    def get_friends(self):
        '''Return all of the friends of this profile.'''
        friend1_profiles = Profile.objects.filter(profile2__profile1=self)
        friend2_profiles = Profile.objects.filter(profile1__profile2=self)

        return (friend1_profiles | friend2_profiles).distinct()
    
    def add_friend(self, other):
        '''Add a friend to this profile.'''
        if other in self.get_friends() or self == other:
            return "Cannot add friend."
        else:
            Friend.objects.create(profile1=self, profile2=other)
            return "Friend added successfully."
        
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
    
    def get_news_feed(self):
        profile_sm = self.get_status_messages()
        friends = self.get_friends()
        newsfeed = set(profile_sm) 
        for f in friends:
            for m in f.get_status_messages():
                newsfeed.add(m)
        return list(newsfeed)
    
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
    

class Friend(models.Model):
    '''Friend class for mini_fb.'''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this StatusMessage object.'''
        return f'{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}'
