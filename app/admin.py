from django.contrib import admin

# Register your models here.
from app.models import*
admin.site.site_heade='Next Clone||Admin'
admin.site.register(Movie)
admin.site.register(Movielist)
admin.site.register(Genre)