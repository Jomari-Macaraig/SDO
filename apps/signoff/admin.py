from django.contrib import admin
from .models import Signoff
from .constants import Status


class SignoffAdmin(admin.ModelAdmin):
    list_display = ("id", "created_time", "user", "stage", "status")
    readonly_fields = (
        "user",
        "opportunity",
        "stage",
        "sub_stage",
        "turn_around_time",
        # "status",
    )
    fields = ("user", "opportunity", "stage", "sub_stage", "turn_around_time", "status")

    def get_readonly_fields(self, request, obj=None):
        read_only_fields = list(super().get_readonly_fields(request=request, obj=obj))
        if obj and obj.status in (Status.APPROVED.value, Status.REJECTED.value):
            read_only_fields.append("status")
        return read_only_fields

    def has_change_permission(self, request, obj=None):
        has_change_permission = super().has_change_permission(request=request, obj=obj)

        if obj and obj.user != request.user:
            return False

        return has_change_permission


admin.site.register(Signoff, SignoffAdmin)
