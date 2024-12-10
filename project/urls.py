'''
Camille Christie
U89708684
camchris@bu.edu
URLS for Music Network project (CS412 final project)
'''

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ShowAllProfilesView, ShowAllInstrumentsView, EditProfileView, ShowProfileView, ShowAllJobPostsView, ShowAllMediaPostsView, ShowMediaPostView, ShowJobPostView, ShowInstrumentProfilesView, CreateNewProfileView, ShowSuggestionsView, CreateNewFriendView, CreateNewUserInstrumentView, ShowSuggestedInstrumentsView, CreateJobPostView, CreateMediaPostView, EditJobPostView, EditMediaPostView, DeleteJobPostView
urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_profiles'),
    path('new_profile', CreateNewProfileView.as_view(), name='create_new_profile'),
    path('instruments', ShowAllInstrumentsView.as_view(), name='show_instruments'),
    path('instruments/<int:pk>', ShowInstrumentProfilesView.as_view(), name='show_instrument_profiles'),
    path('instruments/add_instrument', ShowSuggestedInstrumentsView.as_view(), name='add_instruments'), 
    path('instruments/add_instrument/<int:other_pk>', CreateNewUserInstrumentView.as_view(), name='add_instrument'), 
    path('jobs', ShowAllJobPostsView.as_view(), name='job_posts'),
    path('jobs/<int:pk>', ShowJobPostView.as_view(), name='show_jobpost'),
    path('profile/create_jobpost', CreateJobPostView.as_view(), name='create_jobpost'),
    path('profile/create_mediapost', CreateMediaPostView.as_view(), name='create_mediapost'),
    path('profile/<int:pk>/edit_jobpost', EditJobPostView.as_view(), name='edit_jobpost'), 
    path('profile/<int:pk>/delete_jobpost', DeleteJobPostView.as_view(), name='delete_jobpost'),
    path('profile/<int:pk>/edit_mediapost', EditMediaPostView.as_view(), name='edit_mediapost'), 
    path('newsfeed', ShowAllMediaPostsView.as_view(), name='media_posts'),
    path('newsfeed/<int:pk>', ShowMediaPostView.as_view(), name='show_mediapost'),
    path('profile/<int:pk>', ShowProfileView.as_view(), name='show_profile'),
    path('profile/edit_profile', EditProfileView.as_view(), name='edit_profile'),
    path('profile/friend_suggestions', ShowSuggestionsView.as_view(), name='suggest_friends'),
    path('profile/add_friend/<int:other_pk>', CreateNewFriendView.as_view(), name='add_friend'), 
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logout.html'), name='logout'),

]