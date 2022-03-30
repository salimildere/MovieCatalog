from unittest import mock

from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movie_catalog.catalogs.models import Catalog
from movie_catalog.catalogs.tests.factories import CatalogFactory
from movie_catalog.utils.tests.mocked_responses.helpers import get_mocked_response


class CatalogViewSetTestCase(APITestCase):
    """
    python manage.py test movie_catalog.catalogs.tests.test_views.CatalogViewSetTestCase --keepdb
    """

    def setUp(self):
        CatalogFactory.create_batch(10)
        self.url = reverse("catalogs:catalog")
        self.catalog_field_names = [i.name for i in Catalog._meta.get_fields()]
        self.mocked_service = "movie_catalog.utils.service.ContentService.get_content_from_service"
        self.valid_mock = get_mocked_response(
            "movie_catalog/utils/tests/mocked_responses/data/content_service_id_1_resp.json"
        )
        self.invalid_mock = get_mocked_response(
            "movie_catalog/utils/tests/mocked_responses/data/content_service_empty_response.json"
        )
        cache.clear()

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], Catalog.objects.filter(is_active=True).count())

    def test_response_keys(self):
        response = self.client.get(self.url)
        self.assertEqual(
            set(response.data["results"][0].keys()), set(self.catalog_field_names)
        )

    def test_create(self):
        data = {"title": "Test Catalog", "is_active": True}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["is_active"], data["is_active"])
        self.assertEqual(response.data["id"], Catalog.objects.last().id)

    def test_create_invalid_data(self):
        data = {"is_active": True}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_object_exists(self):
        data = {"title": "Test Catalog", "is_active": True}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_object_exists_inactive(self):
        data = {"title": "Test Catalog", "is_active": False}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_with_content_service_and_invalid_data(self):
        data = {"title": "Test Catalog", "contents": [1]}
        with mock.patch(self.mocked_service, return_value=self.invalid_mock):
            response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_with_content_service_and_valid_data(self):
        data = {"title": "Test Catalog", "contents": [1]}
        with mock.patch(self.mocked_service, return_value=self.valid_mock):
            response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, 201)


class CatalogDetailViewSetTestCase(APITestCase):
    """
    python manage.py test movie_catalog.catalogs.tests.test_views.CatalogDetailViewSetTestCase --keepdb
    """

    def setUp(self):
        self.catalog = CatalogFactory()
        self.url = reverse("catalogs:catalog-detail", kwargs={"pk": self.catalog.pk})
        self.catalog_field_names = [i.name for i in Catalog._meta.get_fields()]
        self.mocked_service = "movie_catalog.utils.service.ContentService.get_content_from_service"
        self.valid_mock = get_mocked_response(
            "movie_catalog/utils/tests/mocked_responses/data/content_service_id_1_resp.json"
        )
        self.invalid_mock = get_mocked_response(
            "movie_catalog/utils/tests/mocked_responses/data/content_service_empty_response.json"
        )
        cache.clear()

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.catalog.title)
        self.assertEqual(response.data["id"], self.catalog.id)

    def test_update(self):
        data = {"title": "Test Catalog", "is_active": True}
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["is_active"], data["is_active"])
        self.assertEqual(response.data["id"], self.catalog.id)

    def test_update_invalid_data(self):
        data = {"is_active": True}
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_update_object_exists(self):
        data = {"title": "Test Catalog", "is_active": True}
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("catalogs:catalog"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_object_exists_inactive(self):
        data = {"title": "Test Catalog", "is_active": False}
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("catalogs:catalog"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_with_content_service_and_invalid_data(self):
        data = {"title": "Test Catalog", "contents": [1]}
        with mock.patch(self.mocked_service, return_value=self.invalid_mock):
            response = self.client.put(self.url, data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update_with_content_service_and_valid_data(self):
        data = {"title": "Test Catalog", "contents": [1]}
        with mock.patch(self.mocked_service, return_value=self.valid_mock):
            response = self.client.put(self.url, data=data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["contents"][0], self.valid_mock["results"][0]["id"])
        self.assertEqual(response.data["id"], self.catalog.id)

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_object_not_exists(self):
        response = self.client.delete(reverse("catalogs:catalog-detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
