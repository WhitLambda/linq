from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from .models import users, user_socials, user_medias

# Register your models here.

admin.site.register(users)
# admin.site.register(users, UserAdmin)
admin.site.register(user_socials)
admin.site.register(user_medias)