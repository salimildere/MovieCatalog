from django.urls import path, include

urlpatterns = [
    # API
    path(
        "v1/catalog/",
        include(("movie_catalog.catalogs.urls", "catalogs"), namespace="catalogs"),
    ),
]
