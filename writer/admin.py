from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class WriterAdmin(UserAdmin):
    list_display = ('full_name', 'bio', 'email', 'is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

from .models import Writer


admin.site.register(Writer, WriterAdmin)