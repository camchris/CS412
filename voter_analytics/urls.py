## hw/urls.py
## description: URL patterns for the hw app

from django.urls import path
from django.conf import settings
from . import views
from .views import VoterListView, VoterDetailView, GraphsListView


# all of the URLs that are part of this app
urlpatterns = [
    path(r'', VoterListView.as_view(), name="voters"),
    path(r'voter/<int:pk>', VoterDetailView.as_view(), name="voter"),
    path(r'graphs', GraphsListView.as_view(), name="graphs"),

]
