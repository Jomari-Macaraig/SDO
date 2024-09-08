from django.contrib.auth.models import User
from django.db import models

from apps.base.models import Audit
from apps.opportunities.models import Opportunity, Stage

from .constants import Status
from .managers import SignoffManager


class Signoff(Audit):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, choices=zip(Status.list(), Status.list()))
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    sub_stage = models.DecimalField(max_digits=4, decimal_places=2)
    turn_around_time = models.PositiveIntegerField()

    objects = SignoffManager()

    def __str__(self):
        return f"{self.user} - {self.opportunity.id}"

    class Meta:
        unique_together = ("user", "opportunity", "status", "sub_stage", "stage")



