from django.contrib import admin

from .models import Warehouse, Good

from simple_history.admin import SimpleHistoryAdmin


class WarehouseAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    fields = ("title", "text", "active", "slug", "created_time")
    readonly_fields = ("slug", "created_time")
    
    list_display = ("title", "active")
    ordering = ("-active", "-created_time")
    list_filter = ("active", )
    
    search_fields = ("title",)


class GoodAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    fields = ("title", "warehouse", ("number", "unit"), "text", "vendor_code", "slug", "created_time")
    readonly_fields = ("slug", "created_time")
    
    list_display = ("title", "warehouse", "number", "unit", )
    ordering = ("-created_time",)
    
    search_fields = ("title",)


admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Good,  GoodAdmin)
