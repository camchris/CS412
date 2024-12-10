from django.urls import path
from .views import ShowAllProfilesView, ShowAllInstrumentsView, EditProfileView, ShowProfileView
urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_profiles'),
    path('instruments', ShowAllInstrumentsView.as_view(), name='show_instruments'),
    path('profile/<int:pk>', ShowProfileView.as_view(), name='show_profile'),
    path('profile/<int:pk>/edit_profile', EditProfileView.as_view(), name='edit_profile'),

]