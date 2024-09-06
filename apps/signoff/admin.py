# from django.contrib import admin
#
# from apps.base.admin import CheckGroupMixins
# from apps.base.constants import Groups
# from .models import SalesAdvisorSignoff, SolutionManagerSignoff, SolutionArchitectSignoff
# from apps.opportunities.constants import Stage
# from apps.opportunities.utils import transition_stage
#
#
# class SolutionArchitectSignoffAdmin(admin.ModelAdmin, CheckGroupMixins):
#     list_display = (
#         "get_opportunity_id",
#         "get_service_delivery_id",
#         "get_sales_advisor",
#         "is_sales_advisor_signoff",
#         "get_solution_manager",
#         "is_solution_manager_signoff",
#     )
#
#     def get_opportunity_id(self, obj):
#         return f"{obj.opportunity.id}"
#
#     get_opportunity_id.short_description = "Opportunity ID"
#     get_opportunity_id.admin_order_field = "opportunity_id"
#
#     def get_service_delivery_id(self, obj):
#         return f"{obj.opportunity.service_delivery_id}"
#
#     get_service_delivery_id.short_description = "Service Delivery ID"
#     get_service_delivery_id.admin_order_field = "service_delivery_id"
#
#     def get_sales_advisor(self, obj):
#         return f"{obj.opportunity.sales_advisor_signoff.user}"
#
#     get_sales_advisor.short_description = "Sales Advisor"
#     get_sales_advisor.admin_order_field = "sales_advisor"
#
#     def get_solution_manager(self, obj):
#         return f"{obj.opportunity.solution_manager_signoff.user}"
#
#     get_solution_manager.short_description = "Solution Manager"
#     get_solution_manager.admin_order_field = "solution_manager"
#
#     def is_sales_advisor_signoff(self, obj):
#         return True if obj.sales_advisor_signoff else False
#
#     is_sales_advisor_signoff.short_description = "Is Sales Advisor Signoff"
#     is_sales_advisor_signoff.admin_order_field = "is_sales_advisor_signoff"
#     is_sales_advisor_signoff.boolean = True
#
#     def is_solution_manager_signoff(self, obj):
#         return True if obj.solution_manager_signoff else False
#
#     is_solution_manager_signoff.short_description = "Is Solution Manager Signoff"
#     is_solution_manager_signoff.admin_order_field = "is_solution_manager_signoff"
#     is_solution_manager_signoff.boolean = True
#
#     def get_readonly_fields(self, request, obj=None):
#         read_only_fields = list(super().get_readonly_fields(request=request, obj=obj))
#         if self.is_sales_advisor_signoff_disabled(request=request, obj=obj):
#             read_only_fields.append("sales_advisor_signoff")
#         if self.is_solution_manager_signoff_disabled(request=request, obj=obj):
#             read_only_fields.append("solution_manager_signoff")
#
#         return read_only_fields
#
#     def is_sales_advisor_signoff_disabled(self, request, obj):
#         has_permission = self.check_group(request=request, group=Groups.SALES_ADVISOR.value)
#
#         if not obj:
#             return True
#
#         return (
#             False
#             if not obj.sales_advisor_signoff
#                 and has_permission
#                 and obj.opportunity.sales_advisor_signoff.user == request.user
#             else True
#         )
#
#     def is_solution_manager_signoff_disabled(self, request, obj):
#         has_permission = self.check_group(request=request, group=Groups.SOLUTION_MANAGER.value)
#
#         if not obj:
#             return True
#
#         return (
#             False
#             if not obj.solution_manager_signoff
#                and has_permission
#                and obj.opportunity.solution_manager_signoff.user == request.user
#             else True
#         )
#
#     def save_model(self, request, obj, form, change):
#         super().save_model(request=request, obj=obj, form=form, change=change)
#         if (
#             obj
#             and obj.sales_advisor_signoff
#             and obj.solution_manager_signoff
#             and obj.opportunity.stage == Stage.INITIAL.value
#         ):
#             transition_stage(opportunity=obj.opportunity, current_stage=Stage.INITIAL)
#
#
# admin.site.register(SalesAdvisorSignoff)
# admin.site.register(SolutionManagerSignoff)
# admin.site.register(SolutionArchitectSignoff, SolutionArchitectSignoffAdmin)
