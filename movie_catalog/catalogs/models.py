from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _

from movie_catalog.utils.models import StarterModel


class Catalog(StarterModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(
        upload_to="catalogs/",
        verbose_name=_("image"),
        null=True,
        blank=True,
    )
    remote_contents_ids = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["order"]
        verbose_name = _("Catalogs")
        verbose_name_plural = _("Catalog")

    def __str__(self):
        return self.title
