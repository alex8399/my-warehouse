from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Shipment, Item

class ShipmentAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    fields = ("number", "slug", "comment", "created_time", "status", "warehouse",)
    readonly_fields = ("slug", "created_time")
    list_display = ("number", "warehouse", "status",)
    list_display_links = ("number",)
    empty_value_display = "-"
    
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.readonly_fields = ("warehouse", "slug", "created_time",)
        else:
            self.readonly_fields = ("slug", "created_time", "status")
        
        return super(ShipmentAdmin, self).get_form(request, obj, **kwargs)


class ShipmentGoodAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    pass

admin.site.register(Shipment, ShipmentAdmin)
admin.site.register(Item,  ShipmentGoodAdmin)
