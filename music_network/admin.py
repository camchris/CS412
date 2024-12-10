from django.contrib import admin

from .models import Profile, Image, Friend, Instrument, UserInstrument, MediaPost, Video, JobPost
admin.site.register(Profile)
admin.site.register(Friend)
admin.site.register(Instrument)
admin.site.register(UserInstrument)
admin.site.register(MediaPost)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(JobPost)

