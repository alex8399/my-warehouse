from django.contrib import admin
from django import forms

from .models import AccessAPI
from simple_history.admin import SimpleHistoryAdmin


class APIAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    fields = ("user", "warehouse", "user_type", "active", "slug", "created_time")
    readonly_fields = ("user", "warehouse", "slug", "created_time")
    list_display = ("user", "warehouse", "user_type", "active")
    list_display_links = ("user", "warehouse")
    empty_value_display = "-"
    
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.fields = ("user", "warehouse", "user_type", "active", "slug", "created_time")
            self.readonly_fields = ("user", "warehouse", "slug", "created_time")
        else:
            self.fields = ("user", "warehouse", "user_type", "active", "slug", "created_time")
            self.readonly_fields = ("slug", "created_time")
        
        return super(APIAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(AccessAPI, APIAdmin)