from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models


class SelfAwareModelMixin:
    def contenttype(self):
        return ContentType.objects.get_for_model(self)

    def contenttype_id(self):
        return self.contenttype().pk

    def app_label(self):
        return self.contenttype().app_label

    def model_name(self):
        return self.contenttype().model


class Audit(models.Model, SelfAwareModelMixin):
    """Base abstract model that provides common audit fields

    All app models should inherit this model

    Ideally, instead of deleting records, we just set the `is_active` field to
    False where possible.

    """
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AppUser(Audit):
    """Base abstract class for models whose records are user-centric

    This class already includes the Audit fields.

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User,
        related_name='+',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    modified_by = models.ForeignKey(
        User,
        related_name='+',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
