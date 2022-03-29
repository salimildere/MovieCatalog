from django.db import models
from django.utils.translation import gettext_lazy as _


class StarterModel(models.Model):
    """
    Base model for all models
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created_at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated_at"))

    class Meta:
        """
        Meta class for all models
        """

        abstract = True
