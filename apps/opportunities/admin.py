from django.contrib import admin

from apps.signoff.models import Signoff
from apps.signoff.constants import Status, SubStage
from .models import Opportunity, Stage, Document


class StageInline(admin.TabularInline):
    model = Stage
    readonly_fields = ("created_time", "stage",)
    fields = ("created_time", "stage")
    can_delete = False
    extra = 0


class SignoffInline(admin.TabularInline):
    model = Signoff
    readonly_fields = (
        "created_time",
        "user",
        "stage",
        "sub_stage",
        "turn_around_time",
        "status",
    )
    fields = (
        "id",
        "created_time",
        "user",
        "stage",
        "sub_stage",
        "turn_around_time",
        "status",
    )
    can_delete = False
    extra = 0


class SignoffUserDedicatedInline(admin.TabularInline):
    model = Signoff
    readonly_fields = (
        "created_time",
        "user",
        "stage",
        "sub_stage",
        "turn_around_time",
    )
    fields = (
        "id",
        "created_time",
        "user",
        "stage",
        "sub_stage",
        "turn_around_time",
        "status",
    )
    can_delete = False
    extra = 0
    verbose_name = "PENDING SIGNOFF"
    verbose_name_plural = "PENDING SIGNOFFS"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(
            user=request.user,
            status=Status.PENDING.value
        )
        return queryset


class DocumentInline(admin.TabularInline):
    model = Document
    fields = (
        "type",
        "document",
    )
    can_delete = False
    extra = 0


class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    inlines = (StageInline, SignoffInline, SignoffUserDedicatedInline, DocumentInline)
    fieldsets = (
        (
            "Information",
            {
                "fields": (
                    "name",
                    "email",
                    "phone_number",
                    "company_name",
                    "service_type",
                    "desired_outcome",
                    "product",
                    "price",
                    "is_sales_qualified",
                    "expected_date",
                ),
                "classes": ("wide", "extrapretty"),
            }
        ),
        (
            "Members",
            {
                "fields": ("sales_advisor", "solution_manager", "solution_architect"),
                "classes": ("wide", "extrapretty"),
            }
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        read_only_fields = list(super().get_readonly_fields(request=request, obj=obj))
        if obj:
            if obj.sales_advisor:
                read_only_fields.append("sales_advisor")
            if obj.solution_manager:
                read_only_fields.append("solution_manager")
            if obj.solution_architect or (not obj.solution_architect and request.user != obj.solution_manager):
                read_only_fields.append("solution_architect")
        else:
            read_only_fields.extend(["sales_advisor", "solution_architect"])
        return read_only_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.sales_advisor = request.user
        super().save_model(request=request, obj=obj, form=form, change=change)
        Opportunity.objects.process_opportunity(opportunity=obj)


admin.site.register(Opportunity, OpportunityAdmin)
