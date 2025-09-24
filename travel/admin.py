from django.contrib import admin

# Register your models here.

from .models import Tour

admin.site.register(Tour)

admin.site.site_header = 'Travel Admin'
admin.site.site_title = 'Travel Admin Portal'
admin.site.index_title = 'Welcome to Travel Admin Portal'

