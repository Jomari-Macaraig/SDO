from django.contrib.auth.models import User
from django.db import models

from apps.base.models import Audit
from apps.opportunities.models import Opportunity, Stage

from .constants import Status


class Signoff(Audit):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, choices=zip(Status.list(), Status.list()))
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "opportunity", "status", "stage")



