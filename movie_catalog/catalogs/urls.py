from django.urls import path

from movie_catalog.catalogs.views import CatalogViewSet, CatalogDetailViewSet

urlpatterns = [
    path("", CatalogViewSet.as_view(), name="catalog"),
    path("<int:pk>/", CatalogDetailViewSet.as_view(), name="catalog-detail"),
]
