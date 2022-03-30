from rest_framework import serializers
from movie_catalog.catalogs.models import Catalog



class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalog
        fields = "__all__"