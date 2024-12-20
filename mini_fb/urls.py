from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView, CreateFriendView, ShowFriendSuggestionsView, ShowNewsFeedView
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('profile/create_status', CreateStatusMessageView.as_view(), name='create_status'), # <int:pk> removed from path
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'), # <int:pk> removed from path
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'), 
    path('profile/add_friend/<int:other_pk>', CreateFriendView.as_view(), name='add_friend'), # <int:pk> removed from path
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='suggest_friends'), # <int:pk> removed from path
    path('profile/news_feed', ShowNewsFeedView.as_view(), name='news_feed'), # <int:pk> removed from path
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
]