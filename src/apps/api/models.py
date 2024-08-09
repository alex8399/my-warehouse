from django.db import models
from django.utils.translation import gettext_lazy as _

from simple_history.models import HistoricalRecords

from utils.models import WideModel, BaseLog
from config.settings.base import AUTH_USER_MODEL

MAX_LENGTH = 255


class AccessAPI(WideModel):
    class UserType(models.TextChoices):
        OWNER = "Owner", _("Owner")
        MANAGER = "Manager", _("Manager")
        LOADER = "Loader", _("Loader")

    slug = models.SlugField(verbose_name="Slug", max_length=MAX_LENGTH,
                            db_index=True, unique=True, editable=False)
    user = models.ForeignKey(verbose_name="User", to=AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="APIs")
    warehouse = models.ForeignKey(verbose_name="Warehouse", to="warehouses.Warehouse",
                                  on_delete=models.CASCADE, related_name="access_APIs")

    active = models.BooleanField(verbose_name="Active", default=True)
    created_time = models.DateTimeField(
        verbose_name="Created time", auto_now_add=True)

    user_type = models.CharField(
        verbose_name="User type", max_length=20, choices=UserType)

    logs = HistoricalRecords(excluded_fields=[
                             "user", "warehouse", "created_time"], cascade_delete_history=True, bases=[BaseLog, ])

    uneditable_validated_fields = ("user", "warehouse",)

    def __eq__(self, other) -> bool:
        reply = False
        if other is not None:
            reply = self.pk == getattr(other, "pk", None)

        return reply

    def __hash__(self) -> int:
        return hash((self.user, self.warehouse))

    def __repr__(self) -> str:
        return self.__str__

    def __str__(self) -> str:
        represenation = "AccessAPI"

        if hasattr(self, "user") and hasattr(self, "warehouse"):
            represenation = "AccessAPI. User: {}. Warehouse: {}.".format(
                self.user.username, self.warehouse.title)

        return represenation

    def is_active(self) -> bool:
        return self.active

    def is_owner(self) -> bool:
        return self.user_type == self.UserType.OWNER

    def is_manager(self) -> bool:
        return self.user_type == self.UserType.MANAGER

    def is_loader(self) -> bool:
        return self.user_type == self.UserType.LOADER

    def has_any_rights(self) -> bool:
        return True

    def can_edit_warehouse(self) -> bool:
        return self.is_owner() and self.is_active()

    def can_delete_warehouse(self) -> bool:
        return self.is_owner() and self.is_active()

    def can_read_warehouse(self) -> bool:
        return self.has_any_rights() and self.is_active()

    def can_read_warehouse_logs(self) -> bool:
        return self.is_owner() and self.is_active()

    def can_create_good(self) -> bool:
        return (self.is_manager() or self.is_owner()) and self.is_active()

    def can_edit_good(self) -> bool:
        return (self.is_manager() or self.is_owner()) and self.is_active()

    def can_delete_good(self) -> bool:
        return (self.is_manager() or self.is_owner()) and self.is_active()

    def can_read_good(self) -> bool:
        return self.has_any_rights() and self.is_active()

    def can_read_good_logs(self) -> bool:
        return self.has_any_rights() and self.is_active()

    def can_create_access_API(self, access_API: 'AccessAPI') -> bool:
        permission = False

        if self.is_active():
            if access_API.is_owner() or access_API.is_manager():
                permission = self.is_owner()
            else:
                permission = self.is_manager() or self.is_owner()

        return permission

    def can_edit_access_API(self, access_API: 'AccessAPI') -> bool:
        permission = False

        if self.is_active():
            if access_API.is_owner():
                permission = False
            elif access_API.is_manager():
                permission = self.is_owner()
            elif access_API.is_loader():
                permission = self.is_manager() or self.is_owner()

        return permission

    def can_delete_access_API(self, access_API: 'AccessAPI') -> bool:
        permission = False

        if self.is_active():
            if access_API.is_owner():
                permission = self == access_API
            elif access_API.is_manager():
                permission = self.is_owner()
            elif access_API.is_loader():
                permission = self.is_manager() or self.is_owner()

        return permission

    def can_read_access_API(self, access_API: 'AccessAPI') -> bool:
        return self.has_any_rights() and self.is_active()

    def can_read_task(self) -> bool:
        return self.has_any_rights() and self.is_active()

    def can_create_task(self) -> bool:
        return (self.is_owner or self.is_manager()) and self.is_active()

    def can_edit_task(self) -> bool:
        return self.has_any_rights() and self.is_active()

    def can_delete_task(self) -> bool:
        return (self.is_owner or self.is_manager()) and self.is_active()
    
    def can_read_task_logs(self) -> bool:
        return self.has_any_rights() and self.is_active()

    def can_read_subtask(self) -> bool:
        return self.has_any_rights() and self.is_active()

    def can_create_subtask(self) -> bool:
        return (self.is_owner or self.is_manager()) and self.is_active()

    def can_edit_subtask(self) -> bool:
        return self.has_any_rights() and self.is_active()

    def can_delete_subtask(self) -> bool:
        return (self.is_owner or self.is_manager()) and self.is_active()
    
    def can_read_subtask_logs(self) -> bool:
        return self.has_any_rights() and self.is_active()

    def can_read_client(self) -> bool:
        return self.has_any_rights() and self.is_active()

    def can_create_client(self) -> bool:
        return (self.is_owner or self.is_manager()) and self.is_active()

    def can_edit_client(self) -> bool:
        return (self.is_owner or self.is_manager()) and self.is_active()

    def can_delete_client(self) -> bool:
        return (self.is_owner or self.is_manager()) and self.is_active()
    
    def can_read_client_logs(self) -> bool:
        return self.has_any_rights() and self.is_active()

    class Meta:
        verbose_name = "Access API"
        verbose_name_plural = "Access APIs"
        unique_together = ('user', 'warehouse')
