from django.contrib import admin
from .models import customUser
# Register your models here.

class AdminUserDetails(admin.ModelAdmin):
    list_display = ['user','contact','dept','year','is_accepted']
admin.site.register(customUser,AdminUserDetails)