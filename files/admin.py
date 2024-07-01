from django.contrib import admin

from files.models import UserFile


@admin.register(UserFile)
class UserFileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserFile._meta.fields]
    list_select_related = ['user']
    search_fields = ['user', 'file']