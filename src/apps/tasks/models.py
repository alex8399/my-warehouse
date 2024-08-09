from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from typing import Sequence

from utils.models import WideModel, BaseLog
from apps.warehouses.models import Warehouse, Good

MAX_LENGTH_CHARFIELD = 255


class Shipment(WideModel):
    class Status(models.TextChoices):
        TO_DO = "To do", _("To do")
        COLLECTING = "Collecting", _("Collecting")
        WAITING_DELIVERY = "Waiting delivery", _("Waiting delivery")
        SENT = "Sent", _("Sent")
        CANCELED = "Canceled", _("Canceled")

    ALLOWED_TRANSCATION = {
        Status.TO_DO: (Status.COLLECTING, Status.CANCELED,),
        Status.COLLECTING: (Status.WAITING_DELIVERY, Status.TO_DO, Status.CANCELED,),
        Status.WAITING_DELIVERY: (Status.SENT, Status.CANCELED,),
        Status.SENT: (Status.CANCELED,),
        Status.CANCELED: (),
    }

    GOOD_CAN_BE_CREATED_STATUSES = (Status.TO_DO,)
    GOOD_STATUS_CAN_BE_CHANGED_STATUSES = (Status.TO_DO, Status.COLLECTING,)
    GOODS_MUST_BE_COMPLETED_STATUSES = (Status.WAITING_DELIVERY, Status.SENT,)

    TAKE_GOODS_FROM_WAREHOUSE_TRANSACTIONS = (
        (Status.WAITING_DELIVERY, Status.SENT),
        (Status.COLLECTING, Status.SENT))
    
    RETURN_GOODS_ON_WAREHOUSE_TRANSACTIONS = (
        (Status.SENT, Status.CANCELED),)

    number = models.SlugField(verbose_name="Internal number", max_length=255)
    slug = models.SlugField(verbose_name="Slug", max_length=255,
                            db_index=True, unique=True, editable=False)
    comment = models.TextField(verbose_name="Comment", blank=True)
    created_time = models.DateTimeField(
        verbose_name="Creation time", auto_now_add=True)

    status = models.CharField(verbose_name="Status", max_length=20,
                              choices=Status, default=Status.TO_DO)
    warehouse = models.ForeignKey(verbose_name="Warehouse", to=Warehouse,
                                  on_delete=models.CASCADE, related_name="shipments")

    logs = HistoricalRecords(excluded_fields=[
                             "slug", "warehouse", "created_time", "number",]
                             , cascade_delete_history=True, bases=[BaseLog, ])

    uneditable_validated_fields = ("warehouse",)

    def __eq__(self, other) -> bool:
        reply = False
        if other is not None:
            reply = self.pk == getattr(other, "pk", None)

        return reply

    def __hash__(self) -> int:
        return hash((self.slug,))
    
    def __str__(self) -> str:
        return "Shipment №{}".format(self.number)
    
    def __repr__(self) -> str:
        return self.__str__()

    def get_logs(self) -> Sequence[HistoricalRecords]:
        return self.logs.all()

    def get_items(self) -> Sequence['Item']:
        return self.goods.all()

    def save(self, *args, **kwargs) -> None:
        if self.is_adding():
            self.status = self.Status.TO_DO

        super().save(*args, **kwargs)
        
    def __validate_shipment_items_statuses(self) -> None:
        if not self.is_adding() and self.status in self.GOODS_MUST_BE_COMPLETED_STATUSES:
            if any(item.status == item.Status.TO_DO for item in self.get_items()):
                raise ValidationError(
                    "Not all goods are collected for shipment.")

    def __validate_status(self) -> None:
        if not self.is_adding():
            loaded_status = self.get_field_from_loaded_state("status")

            if self.status != loaded_status:
                transaction = (loaded_status, self.status)

                if not self.__is_valid_transaction(*transaction):
                    raise ValidationError(
                        "The shipment can not go from status '{}' to status '{}'.".format(
                            loaded_status, self.status))

                if transaction in Shipment.TAKE_GOODS_FROM_WAREHOUSE_TRANSACTIONS:
                    self.__take_goods_from_warehouse()

                if transaction in Shipment.RETURN_GOODS_ON_WAREHOUSE_TRANSACTIONS:
                    self.__return_goods_to_warehouse()

    def __take_goods_from_warehouse(self) -> None:
        for item in self.get_items():
            if item.status == Item.Status.COLLECTED:
                item.good.take(item.number)

    def __return_goods_to_warehouse(self) -> None:
        for item in self.get_items():
            if item.status == Item.Status.COLLECTED:
                item.good.put(item.number)

    def __is_valid_transaction(self, previous_status, currect_status) -> bool:
        valid_transaction = False

        if not self.is_adding() and previous_status != currect_status:
            if currect_status in self.ALLOWED_TRANSCATION[previous_status]:
                valid_transaction = True
        else:
            valid_transaction = True

        return valid_transaction

    def clean(self) -> None:
        self.__validate_shipment_items_statuses()
        self.__validate_status()

        super().clean()

    def can_good_status_be_changed(self) -> bool:
        return self.status in self.GOOD_STATUS_CAN_BE_CHANGED_STATUSES

    def can_good_be_created(self) -> bool:
        return self.status in self.GOOD_CAN_BE_CREATED_STATUSES

    class Meta:
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
        
        unique_together = ("warehouse", "number")


class Item(WideModel):
    class Status(models.TextChoices):
        TO_DO = "To do", _("To do")
        COLLECTED = "Collected", _("Collected")

    slug = models.SlugField(verbose_name="Slug", max_length=255,
                            db_index=True, unique=True, editable=False)

    good = models.ForeignKey(verbose_name="Good", to=Good,
                             on_delete=models.CASCADE, related_name="shipments")
    number = models.BigIntegerField(
        verbose_name="Number", validators=[MinValueValidator(0)])
    task = models.ForeignKey(verbose_name="Task", to=Shipment,
                             on_delete=models.CASCADE, related_name="goods")

    created_time = models.DateTimeField(
        verbose_name="Creation time", auto_now_add=True)
    status = models.CharField(verbose_name="Status", max_length=20,
                              choices=Status, default=Status.TO_DO)

    logs = HistoricalRecords(excluded_fields=[
        "slug", "warehouse", "created_time", "good", "task"], cascade_delete_history=True, bases=[BaseLog, ])

    uneditable_validated_fields = ("good", "number", "task")

    def __eq__(self, other) -> bool:
        reply = False
        if other is not None:
            reply = self.pk == getattr(other, "pk", None)

        return reply

    def __hash__(self) -> int:
        return hash((self.slug,))
    
    
    def __str__(self) -> str:
        return self.good.title
    
    def __repr__(self) -> str:
        return self.__str__()

    def save(self, *args, **kwargs) -> None:
        if self.is_adding():
            self.status = self.Status.TO_DO

        super().save(*args, **kwargs)

    def get_logs(self) -> Sequence[HistoricalRecords]:
        return self.logs.all()

    def __validate_number(self) -> None:
        if self.is_adding() and self.good.get_available_number() < self.number:
            raise ValidationError("There is not enough goods \"{}\" in the warehouse.".format(
                self.good.title.capitalize()))

    def __validate_status(self) -> None:
        if not self.is_adding():
            previous_status = self.get_field_from_loaded_state("status")
            if previous_status != self.status and not self.task.can_good_status_be_changed():
                raise ValidationError(
                    "The status of good can not be changed if shipment status is \"{}\".".format(
                        self.task.status))

    def __validate_task_status(self) -> None:
        if self.is_adding() and not self.task.can_good_be_created():
            raise ValidationError(
                "Shipment good can not be created since the status of task is \"{}\".".format(
                    self.task.status))
            
    def __validate_good(self) -> None:
        if self.good.warehouse != self.task.warehouse:
            raise ValidationError("The good can not be attached to task which does not belong to warehouse.")

    def clean(self) -> None:
        self.__validate_task_status()
        self.__validate_number()
        self.__validate_status()
        self.__validate_good()
        
        super().clean()

    class Meta:
        verbose_name = "Item in shipment"
        verbose_name_plural = "Items in shipment"
        unique_together = ("good", "task")
