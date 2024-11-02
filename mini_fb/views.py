from .models import Profile, Image, StatusMessage, Friend
import random
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm
        return context
    
    def form_valid(self, form):
        '''
        Handle the form submission. 
        '''
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        form.instance.user = user
        return super().form_valid(form)


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to create a new status message and save it to the database.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Profile to the StatusMessage object.
        We can find the PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        profile = self.get_object()
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files') 
        for file in files:
            image = Image(status_message=sm, image_file=file)
            image.save()
        return super().form_valid(form)
    
    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all_profiles')
        return reverse('show_profile', kwargs={'pk': self.get_object().pk})
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to update a profile and save it to the database.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)


    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a status message'''
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'message'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_success_url(self) -> str:
        profile_pk = self.get_object().profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''A view to update a status message and save it to the database.'''
    model = StatusMessage
    template_name = "mini_fb/update_status_form.html"
    context_object_name = 'message'

    fields = ['message', ]

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_success_url(self) -> str:
        profile_pk = self.get_object().profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class CreateFriendView(LoginRequiredMixin, View):
    '''A view to create a friend relationship and save it to the database.'''

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)
    
    def dispatch(self, request, *args, **kwargs):
        friend_pk = kwargs.get('other_pk')
        
        profile = self.get_object()
        friend_profile = get_object_or_404(Profile, id=friend_pk)
        
        result = profile.add_friend(friend_profile)
        
        return HttpResponseRedirect(reverse('show_profile', kwargs={'pk': profile.pk}))
    
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    '''A view to suggest friends to a user.'''
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = 'profile'

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    '''A view to view the newsfeed of a user.'''
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = 'profile'

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    



    