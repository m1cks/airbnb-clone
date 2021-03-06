from django.contrib import admin
from django.utils import timezone
from . import models


# Filter for progress reservation
class ProgressListFilter(admin.SimpleListFilter):
    title = "In Progress"
    parameter_name = "in_progress"

    def lookups(self, request, model_admin):
        return (
            ("True", "True"),
            ("False", "False"),
        )

    def queryset(self, request, queryset):
        now = timezone.now().date()

        if self.value() == "True":
            return queryset.filter(check_in__lt=now, check_out__gt=now)

        elif self.value() == "False":
            return queryset.exclude(check_in__lt=now, check_out__gt=now)


# Filter for finished reservation
class FinishedListFilter(admin.SimpleListFilter):
    title = "Is Finished"
    parameter_name = "is_finished"

    def lookups(self, request, model_admin):
        return (
            ("True", "True"),
            ("False", "False"),
        )

    def queryset(self, request, queryset):
        now = timezone.now().date()

        if self.value() == "True":
            return queryset.filter(check_out__lte=now)

        elif self.value() == "False":
            return queryset.exclude(check_out__lte=now)


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """Reservation Admin Definition"""

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status", ProgressListFilter, FinishedListFilter)


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    list_display = ("day", "reservation")
