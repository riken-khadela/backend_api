from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,instagram_accounts, SearchedHistory

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", 'is_user_verified']


class SearchedHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'hashtag', 'result', 'platform', 'created']
    search_fields = ['user__username', 'hashtag']
    list_filter = ['platform', 'created']

admin.site.register(SearchedHistory, SearchedHistoryAdmin)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(instagram_accounts)

