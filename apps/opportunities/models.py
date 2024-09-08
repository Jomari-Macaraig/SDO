from django.contrib.auth.models import User
from django.db import models

from apps.base.models import Audit
from .constants import Stage as StageEnum, DocumentType
from .managers import OpportunityManager


class Opportunity(Audit):

    name = models.CharField(max_length=64)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    company_name = models.CharField(max_length=24, null=True, blank=True)
    service_type = models.CharField(max_length=24)
    desired_outcome = models.TextField()
    product = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Price (USD)")
    is_sales_qualified = models.BooleanField()
    expected_date = models.DateField()

    sales_advisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales_advisor_opportunities")
    solution_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="solution_manager_opportunities"
    )
    solution_architect = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="solution_architect_opportunities"
    )

    objects = OpportunityManager()

    def __str__(self):
        return self.name

    def initialize_stage(self):
        self.stage_set.add(Stage.objects.create(opportunity=self, stage=StageEnum.INITIAL.value))

    class Meta:
        verbose_name = "Opportunity"
        verbose_name_plural = "Opportunities"


class Stage(Audit):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    stage = models.CharField(max_length=64, choices=zip(StageEnum.list(), StageEnum.list()))

    def __str__(self):
        return f"{self.opportunity.name} - {self.stage}"

    class Meta:
        unique_together = ("opportunity", "stage")


class Document(Audit):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    type = models.CharField(max_length=64, choices=zip(DocumentType.list(), DocumentType.list()))
    document = models.FileField()
