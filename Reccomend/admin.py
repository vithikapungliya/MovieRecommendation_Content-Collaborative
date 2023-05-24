from django.contrib import admin
from .models import Training,Questionnaire, Movie, Playlist
# Register your models here.
admin.site.register(Movie)
admin.site.register(Training)
admin.site.register(Questionnaire)
admin.site.register(Playlist)