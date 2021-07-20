from django.contrib import admin
from .models import user_profile, Contact
# Register your models here.

admin.site.register(user_profile)
admin.site.register(Contact)