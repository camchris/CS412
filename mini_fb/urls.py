from django.urls import path
from django.conf import settings
from . import views
from .views import ShowAllProfilesView
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'), # generic class-based view
]