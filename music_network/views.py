from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from .models import Profile, Instrument
from .forms import EditProfileForm

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile # retrieve objects from the database
    template_name = 'music_network/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfileView(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'music_network/show_profile.html'
    context_object_name = 'profile'

class EditProfileView(UpdateView): # incorporate login mixin
    '''A view to update a profile and save it to the database.'''
    model = Profile
    form_class = EditProfileForm
    template_name = "music_network/edit_profile.html"

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)


    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')


class ShowAllInstrumentsView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Instrument # retrieve objects from the database
    template_name = 'music_network/show_all_instruments.html'
    context_object_name = 'instruments' # how to find the data in the template file