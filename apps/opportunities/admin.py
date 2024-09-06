from django.contrib import admin

from .models import Opportunity, Stage
from apps.signoff.models import Signoff


class StageInline(admin.TabularInline):
    model = Stage
    readonly_fields = ("created_time", "stage",)
    fields = ("created_time", "stage")
    can_delete = False
    extra = 0


class SignoffInline(admin.TabularInline):
    model = Signoff
    readonly_fields = ("created_time", "user", "stage")
    fields = ("created_time", "user", "stage", "status")
    can_delete = False
    extra = 0


class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    inlines = (StageInline, SignoffInline)
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
            if obj.solution_architect:
                read_only_fields.append("solution_architect")
        else:
            read_only_fields.extend(["sales_advisor", "solution_architect"])
        return read_only_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.sales_advisor = request.user
        super().save_model(request=request, obj=obj, form=form, change=change)
        if not change:
            obj.initialize_stage()


admin.site.register(Opportunity, OpportunityAdmin)
#
#
# class OpportunityAdmin(admin.ModelAdmin, CheckGroupMixins):
#     list_display = ("id", "service_delivery_id", "name", "service_type", "stage")
#     list_filter = ("stage",)
#     readonly_fields = (
#         "stage",
#         "initial_start_date",
#         "initial_end_date",
#         "scoping_start_date",
#         "scoping_end_date",
#     )
#     fieldsets = (
#         (
#             "Basic Information",
#             {
#                 "fields": (
#                     "created_by",
#                     "modified_by",
#                     "user",
#                 ),
#                 "classes": ("wide", "extrapretty"),
#             }
#         ),
#         (
#             "Information",
#             {
#                 "fields": (
#                     "service_delivery_id",
#                     "name",
#                     "email",
#                     "phone_number",
#                     "company_name",
#                     "service_type",
#                     "desired_outcome",
#                     "product",
#                     "price",
#                     "is_sales_qualified",
#                     "expected_date",
#                     "stage",
#                     "bid",
#                 ),
#                 "classes": ("wide", "extrapretty"),
#             }
#         ),
#         (
#             "Auditing",
#             {
#                 "fields": (
#                     "initial_start_date",
#                     "initial_end_date",
#                     "scoping_start_date",
#                     "scoping_end_date",
#                 ),
#                 "classes": ("wide", "extrapretty"),
#             }
#         ),
#         (
#             "Signoff",
#             {
#                 "fields": ("sales_advisor_signoff", "solution_manager_signoff", "solution_architect_signoff"),
#                 "classes": ("wide", "extrapretty"),
#             }
#         ),
#     )
#
#     def get_readonly_fields(self, request, obj=None):
#         read_only_fields = list(super().get_readonly_fields(request=request, obj=obj))
#         if self.is_sales_advisor_signoff_disabled(request=request, obj=obj):
#             read_only_fields.append("sales_advisor_signoff")
#         if self.is_solution_manager_signoff_disabled(request=request, obj=obj):
#             read_only_fields.append("solution_manager_signoff")
#         if self.is_solution_architect_signoff_disabled(request=request, obj=obj):
#             read_only_fields.append("solution_architect_signoff")
#
#         return read_only_fields
#
#     def is_sales_advisor_signoff_disabled(self, request, obj):
#         has_permission = self.check_group(request=request, group=Groups.SALES_ADVISOR.value)
#         return (
#             True
#             if not obj or obj.sales_advisor_signoff or not has_permission else
#             False
#         )
#
#     def is_solution_manager_signoff_disabled(self, request, obj):
#         has_permission = self.check_group(request=request, group=Groups.SOLUTION_MANAGER.value)
#         return (
#             True
#             if not obj or obj.solution_manager_signoff
#                 or not obj.sales_advisor_signoff
#                 or not has_permission
#                 or request.user != obj.sales_advisor_signoff.assignee
#             else False
#         )
#
#     def is_solution_architect_signoff_disabled(self, request, obj):
#         has_permission = self.check_group(request=request, group=Groups.SOLUTION_ARCHITECT.value)
#         return (
#             True
#             if not obj
#                 or obj.solution_architect_signoff
#                 or not obj.solution_manager_signoff
#                 or not obj.sales_advisor_signoff
#                 or not has_permission
#                 or request.user != obj.solution_manager_signoff.assignee
#             else False
#         )
#
#
# admin.site.register(Opportunity, OpportunityAdmin)
