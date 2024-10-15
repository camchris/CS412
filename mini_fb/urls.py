from django.urls import path
from django.conf import settings
from . import views
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
    #path('create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
]