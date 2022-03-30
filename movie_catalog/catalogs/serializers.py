from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movie_catalog.catalogs.models import Catalog
from movie_catalog.utils.service import ContentService


class CatalogSerializer(serializers.ModelSerializer):
    content_service = ContentService()

    class Meta:
        model = Catalog
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if not is_valid:
            return is_valid

        if contents := self.validated_data.get('contents'):
            try:
                value = self.content_service.is_valid_content_list(contents, raise_exception)
            except:
                raise ValidationError('Invalid content list')
            return value
        return True
