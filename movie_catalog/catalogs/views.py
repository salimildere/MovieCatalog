from rest_framework import generics

from movie_catalog.catalogs.models import Catalog
from movie_catalog.catalogs.serializers import CatalogSerializer


class CatalogViewSet(generics.ListCreateAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class CatalogDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
