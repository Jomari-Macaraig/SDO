from django.utils import timezone

from .models import Opportunity
from .constants import Stage


def transition_stage(opportunity: Opportunity, current_stage: Stage):
    if current_stage == Stage.INITIAL:
        opportunity.stage = Stage.SCOPING.value
        opportunity.initial_end_date = timezone.now()
        opportunity.scoping_start_date = timezone.now()
        opportunity.save()