from .models import Profile, Image, StatusMessage
import random
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm


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
        sm = form.save()
        files = self.request.FILES.getlist('files') 
        for file in files:
            image = Image(status_message=sm, image_file=file)
            image.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all_profiles')
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
class UpdateProfileView(UpdateView):
    '''A view to update a profile and save it to the database.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

class DeleteStatusMessageView(DeleteView):
    '''A view to delete a status message'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'message'

    def get_success_url(self) -> str:
        profile_pk = self.get_object().profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class UpdateStatusMessageView(UpdateView):
    '''A view to update a status message and save it to the database.'''
    model = StatusMessage
    template_name = "mini_fb/update_status_form.html"
    context_object_name = 'message'

    fields = ['message', ]

    def get_success_url(self) -> str:
        profile_pk = self.get_object().profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})



    