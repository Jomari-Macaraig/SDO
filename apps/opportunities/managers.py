from django.db.models import Manager

from apps.signoff.constants import SubStage
from .constants import DocumentType


class OpportunityManager(Manager):

    def _process_one_dot_one(self, opportunity):
        opportunity.initialize_stage()
        opportunity.signoff_set.process_stage(opportunity=opportunity, sub_stage=SubStage.ONE_DOT_ONE)

    def _process_one_dot_two(self, opportunity):
        opportunity.signoff_set.process_stage(opportunity=opportunity, sub_stage=SubStage.ONE_DOT_TWO)

    def _process_one_dot_three(self, opportunity):
        opportunity.signoff_set.process_stage(opportunity=opportunity, sub_stage=SubStage.ONE_DOT_THREE)


    def process_opportunity(self, opportunity):
        if not opportunity.stage_set.count():
            self._process_one_dot_one(opportunity=opportunity)
        elif (
                opportunity.solution_architect
                and not opportunity.signoff_set.filter(sub_stage=SubStage.ONE_DOT_THREE.value).count()
        ):
            self._process_one_dot_two(opportunity=opportunity)
        elif (
            not opportunity.signoff_set.filter(sub_stage=SubStage.ONE_DOT_FOUR.value).count()
            and not opportunity.document_set.filter(type=DocumentType.SERVICE_DELIVERY_OUTPUT).count()
        ):
            self._process_one_dot_three(opportunity=opportunity)