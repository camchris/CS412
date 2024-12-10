'''
Camille Christie
U89708684
camchris@bu.edu
Views for Music Network project (CS412 final project)
'''

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View, DeleteView
from .models import Profile, Instrument, JobPost, MediaPost, Image, Video
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditProfileForm, CreateNewProfileForm, CreateJobPostForm, CreateMediaPostForm
from django.contrib.auth.forms import UserCreationForm

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile # retrieve objects from the database
    template_name = 'project/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfileView(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'project/show_profile.html'
    context_object_name = 'profile'

class CreateNewProfileView(CreateView):
    '''A view to create a new profile and save it to the database.'''
    form_class = CreateNewProfileForm
    template_name = "project/create_profile_form.html"

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

class EditProfileView(LoginRequiredMixin, UpdateView): # incorporate login mixin
    '''A view to update a profile and save it to the database.'''
    model = Profile
    form_class = EditProfileForm
    template_name = "project/edit_profile.html"

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)


    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
class ShowSuggestionsView(LoginRequiredMixin, DetailView):
    '''A view to suggest friends to a user.'''
    model = Profile
    template_name = "project/friend_suggestions.html"
    context_object_name = 'profile'

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')


class ShowAllInstrumentsView(ListView):
    '''Create a subclass of ListView to display all instruments.'''
    model = Instrument # retrieve objects from the database
    template_name = 'project/show_all_instruments.html'
    context_object_name = 'instruments' # how to find the data in the template file

class ShowSuggestedInstrumentsView(LoginRequiredMixin, DetailView):
    '''Create a subclass of DetailView to display suggested instruments.'''
    model = Profile
    template_name = "project/add_instruments.html"
    context_object_name = 'profile'

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

class ShowAllMediaPostsView(DetailView):
    '''subclass of listview to display all media posts'''

    model = Profile
    template_name = 'project/display_mediaposts.html'
    context_object_name = 'profile'

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

class ShowAllJobPostsView(ListView):
    '''subclass of listview to display all job posts'''
    model = JobPost
    template_name = 'project/display_jobposts.html'
    context_object_name = 'job_posts'

    def get_queryset(self):
        '''Filter job posts based on minimum pay, maximum pay, and instrument.'''
        queryset = super().get_queryset()
        min_pay = self.request.GET.get('min_pay')
        max_pay = self.request.GET.get('max_pay')
        instrument = self.request.GET.get('instrument')

        if min_pay:
            queryset = queryset.filter(pay__gte=min_pay)
        if max_pay:
            queryset = queryset.filter(pay__lte=max_pay)
        if instrument:
            queryset = queryset.filter(instrument__id=instrument)

        return queryset

    def get_context_data(self, **kwargs):
        '''Add context to the template.'''
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['instruments'] = Instrument.objects.all()  # pass all instruments to the template
        return context
    

class ShowMediaPostView(LoginRequiredMixin, DetailView):
    '''Show the details for one media post.'''
    model = MediaPost
    template_name = 'project/show_mediapost.html'
    context_object_name = 'post'


class ShowJobPostView(DetailView):
    '''Show the details for one job post.'''
    model = JobPost
    template_name = 'project/show_jobpost.html'
    context_object_name = 'post'

class CreateJobPostView(LoginRequiredMixin, CreateView):
    '''A view to create a new jobpost and save it to the database.'''
    form_class = CreateJobPostForm
    template_name = "project/create_jobpost_form.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Profile to the JobPost object.
        We can find the PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        profile = self.get_object()
        form.instance.profile = profile
        return super().form_valid(form)
    
    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)
    
    def get_form(self, *args, **kwargs):
        '''Dynamically set the queryset for the instrument field.'''
        form = super().get_form(*args, **kwargs)
        form.fields['instrument'].queryset = Instrument.objects.all()  # Populate instruments dynamically
        return form

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('show_profile', kwargs={'pk': self.get_object().pk})
    
class EditJobPostView(LoginRequiredMixin, UpdateView):
    '''A view to update a jobpost and save it to the database.'''
    model = JobPost
    template_name = "project/edit_jobpost.html"
    context_object_name = 'jobpost'

    fields = ['description', 'pay', 'location' ]

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_success_url(self) -> str:
        profile_pk = self.get_object().profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class DeleteJobPostView(LoginRequiredMixin, DeleteView):
    '''A view to delete a jobpost'''
    model = JobPost
    template_name = 'project/delete_jobpost.html'
    context_object_name = 'jobpost'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_success_url(self) -> str:
        profile_pk = self.get_object().profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class CreateMediaPostView(LoginRequiredMixin, CreateView):
    '''A view to create a new mediapost and save it to the database.'''
    form_class = CreateMediaPostForm
    template_name = "project/create_mediapost.html"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Profile to the MediaPost object.
        We can find the PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        profile = self.get_object()
        form.instance.profile = profile
        mp = form.save()
        files = self.request.FILES.getlist('files') 
        for file in files:
            if file.content_type.startswith('image/'):
                # save image file
                image = Image(media_post=mp, image_file=file)
                image.save()
            elif file.content_type.startswith('video/'):
                # save video file
                video = Video(media_post=mp, video_file=file)
                video.save()
        return super().form_valid(form)
    
    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)
    
    def get_form(self, *args, **kwargs):
        '''Dynamically set the queryset for the instrument field.'''
        form = super().get_form(*args, **kwargs)
        return form

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all_profiles')
        return reverse('show_profile', kwargs={'pk': self.get_object().pk})
    
class EditMediaPostView(LoginRequiredMixin, UpdateView):
    '''A view to update a mediapost and save it to the database.'''
    model = MediaPost
    template_name = "project/edit_mediapost.html"
    context_object_name = 'mediapost'

    fields = ['message' ]

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')

    def get_success_url(self) -> str:
        profile_pk = self.get_object().profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})

class ShowInstrumentProfilesView(DetailView):
    '''Create a subclass of ListView to display profiles that play a particular instrument.'''
    model = Instrument # retrieve objects from the database
    template_name = 'project/show_instrument_profiles.html'
    context_object_name = 'instrument' # how to find the data in the template file

class CreateNewFriendView(LoginRequiredMixin, View):
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
    
class CreateNewUserInstrumentView(LoginRequiredMixin, View):
    '''A view to create a user/instrument relationship and save it to the database.'''

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)
    
    def dispatch(self, request, *args, **kwargs):
        instrument_pk = kwargs.get('other_pk')
        
        profile = self.get_object()
        instrument = get_object_or_404(Instrument, id=instrument_pk)
        
        result = profile.add_instrument(instrument)
        
        return HttpResponseRedirect(reverse('show_profile', kwargs={'pk': profile.pk}))

    

