from django.db.models import Manager

from .constants import SubStage, Status

from apps.opportunities.models import Opportunity


class SignoffManager(Manager):

    def _process_one_dot_one(self, opportunity: Opportunity):
        self.model.objects.create(
            user=opportunity.sales_advisor,
            opportunity=opportunity,
            status=Status.APPROVED.value,
            sub_stage=SubStage.ONE_DOT_ONE.value,
            turn_around_time=1,
            stage=opportunity.stage_set.order_by("-created_time").first(),
        )

        self.model.objects.create(
            user=opportunity.solution_manager,
            opportunity=opportunity,
            status=Status.PENDING.value,
            sub_stage=SubStage.ONE_DOT_TWO.value,
            turn_around_time=1,
            stage=opportunity.stage_set.order_by("-created_time").first(),
        )

    def _process_one_dot_two(self, opportunity: Opportunity):
        solution_manager_signoff = opportunity.signoff_set.get(sub_stage=SubStage.ONE_DOT_TWO.value)
        solution_manager_signoff.status = Status.APPROVED.value
        solution_manager_signoff.save()

        self.model.objects.create(
            user=opportunity.solution_architect,
            opportunity=opportunity,
            status=Status.PENDING.value,
            sub_stage=SubStage.ONE_DOT_THREE.value,
            turn_around_time=2,
            stage=opportunity.stage_set.order_by("-created_time").first(),
        )

    def _process_one_dot_three(self, opportunity: Opportunity):
        solution_architect_signoff = opportunity.signoff_set.get(sub_stage=SubStage.ONE_DOT_THREE.value)
        solution_architect_signoff.status = Status.APPROVED.value
        solution_architect_signoff.save()

        self.model.objects.create(
            user=opportunity.sales_advisor,
            opportunity=opportunity,
            status=Status.PENDING.value,
            sub_stage=SubStage.ONE_DOT_FOUR.value,
            turn_around_time=1,
            stage=opportunity.stage_set.order_by("-created_time").first(),
        )
        self.model.objects.create(
            user=opportunity.solution_architect,
            opportunity=opportunity,
            status=Status.PENDING.value,
            sub_stage=SubStage.ONE_DOT_FOUR.value,
            turn_around_time=1,
            stage=opportunity.stage_set.order_by("-created_time").first(),
        )

    def process_stage(self, opportunity: Opportunity, sub_stage: SubStage):
        mappings = {
            SubStage.ONE_DOT_ONE: self._process_one_dot_one,
            SubStage.ONE_DOT_TWO: self._process_one_dot_two,
            SubStage.ONE_DOT_THREE: self._process_one_dot_three,
        }
        function = mappings.get(sub_stage)
        if function:
            function(opportunity=opportunity)