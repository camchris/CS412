from .models import Profile
import random
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm


class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile # retrieve objects from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfilePageView(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    '''A view to create a new profile and save it to the database.'''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

class CreateStatusMessageView(CreateView):
    '''A view to create a new status message and save it to the database.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Profile to the StatusMessage object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all_profiles')
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})


    