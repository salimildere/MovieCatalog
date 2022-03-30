from rest_framework import generics

from movie_catalog.catalogs.models import Catalog
from movie_catalog.catalogs.serializers import CatalogSerializer
from movie_catalog.utils.service import ContentService


class CatalogViewSet(generics.ListCreateAPIView):
    queryset = Catalog.objects.filter(is_active=True).order_by("order")
    serializer_class = CatalogSerializer

class CatalogDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    content_service = ContentService()

    def get_object(self):
        obj = super(CatalogDetailViewSet, self).get_object()
        if obj.contents_ids:
            data = self.content_service.get_content_list(obj.contents_ids)
            obj.contents_ids = data
        return obj