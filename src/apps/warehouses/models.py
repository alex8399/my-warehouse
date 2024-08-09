from django.db import models
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Sum, Count
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from typing import Sequence

from utils.models import WideModel, BaseLog
from apps.api.models import AccessAPI
from apps.accounts.models import User


class Warehouse(WideModel):
    title = models.CharField(verbose_name="Title", max_length=255)
    slug = models.SlugField(verbose_name="Slug", max_length=255,
                            db_index=True, unique=True, editable=False)
    text = models.TextField(verbose_name="Description", blank=True)
    active = models.BooleanField(verbose_name="Actitve", default=True)
    created_time = models.DateTimeField(
        verbose_name="Creation time", auto_now_add=True)

    logs = HistoricalRecords(excluded_fields=["slug", "text", "created_time"],
                             cascade_delete_history=True, bases=[BaseLog],)

    def __eq__(self, other) -> bool:
        reply = False
        if other is not None:
            reply = self.pk == getattr(other, "pk", None)

        return reply

    def __hash__(self) -> int:
        return hash((self.slug,))

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.title

    def get_goods(self) -> Sequence['Good']:
        return self.goods.all()

    def get_access_APIs(self) -> Sequence['AccessAPI']:
        return self.access_APIs.all()

    def get_logs(self) -> Sequence[HistoricalRecords]:
        return self.logs.all()

    def get_shipments(self) -> Sequence['Shipments']:
        return self.shipments.all()

    def is_active(self) -> bool:
        return self.active

    def create_access_API_for_initial_user(self, user: User) -> AccessAPI:
        initial_user_acccess_API = AccessAPI.objects.create(
            warehouse=self, user=user, user_type=AccessAPI.UserType.OWNER)
        return initial_user_acccess_API

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"


class Good(WideModel):
    class Unit(models.TextChoices):
        PIECE = "P", _("Piece(s)")
        METER = "M", _("Meter(s)")
        KILOGRAM = "KG", _("Kilogram(s)")
        LITER = "L", _("Liter(s)")
        SQUARE_METER = "M^2", _("Square meter(s)")
        NON_DEFINED_UNIT = "ND", _("Non defined unit(s)")

    title = models.CharField(verbose_name="Title", max_length=255)
    slug = models.SlugField(verbose_name="Slug", max_length=255,
                            db_index=True, unique=True)
    warehouse = models.ForeignKey(verbose_name="Warehouse", to=Warehouse,
                                  on_delete=models.CASCADE, related_name="goods")

    vendor_code = models.CharField(
        verbose_name="Vendor code", max_length=255, blank=True)
    text = models.TextField(verbose_name="Description", blank=True)

    number = models.BigIntegerField(
        verbose_name="Number", validators=[MinValueValidator(0)])
    unit = models.CharField(verbose_name="Unit", max_length=20,
                            choices=Unit, default=Unit.PIECE)

    created_time = models.DateTimeField(
        verbose_name="Creation time", auto_now_add=True)

    logs = HistoricalRecords(excluded_fields=["slug", "warehouse", "created_time"],
                             cascade_delete_history=True, bases=[BaseLog, ])

    uneditable_validated_fields = ("warehouse",)

    def __eq__(self, other) -> bool:
        reply = False
        if other is not None:
            reply = self.pk == getattr(other, "pk", None)

        return reply

    def __hash__(self) -> int:
        return hash((self.slug,))

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.title

    def get_logs(self) -> list:
        return self.logs.all()

    def get_reserved_number(self) -> int:
        waiting_shipments = self.shipments.filter(
            ~Q(task__status="SENT") & ~Q(task__status="CANCELED"))

        reserved_number = 0
        if len(waiting_shipments) > 0:
            reserved_number = waiting_shipments.aggregate(
                total_number=Sum("number"))["total_number"]

        return reserved_number

    def get_available_number(self) -> int:
        return self.number - self.get_reserved_number()

    def take(self, number: int):
        self.number -= number
        self.save()

    def put(self, number: int):
        self.number += number
        self.save()

    class Meta:
        verbose_name = "Good"
        verbose_name_plural = "Goods"
