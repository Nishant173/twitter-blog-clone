from django.contrib import admin
from .models import Profile, Follower


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )


class FollowerAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
    search_fields = ('follower', 'following')


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follower, FollowerAdmin)