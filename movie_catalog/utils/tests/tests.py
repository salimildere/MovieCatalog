from unittest import TestCase, mock
from django.core.cache import cache
from movie_catalog.utils.service import ContentService
from movie_catalog.utils.tests.mocked_responses.helpers import get_mocked_response


class ContentServiceTestCase(TestCase):
    """
    python manage.py test movie_catalog.utils.tests.tests.ContentServiceTestCase  --keepdb
    """
    def setUp(self):
        self.service = ContentService()
        self.mocked_service = "movie_catalog.utils.service.ContentService.get_content_from_service"
        self.valid_mock = get_mocked_response(
            "movie_catalog/utils/tests/mocked_responses/data/content_service_id_1_resp.json"
        )
        self.invalid_mock = get_mocked_response(
            "movie_catalog/utils/tests/mocked_responses/data/content_service_empty_response.json"
        )
        cache.clear()

    def test_is_valid_content_list_returns_true(self):
        with mock.patch(self.mocked_service, return_value=self.valid_mock):
            self.assertTrue(self.service.is_valid_content_list([1]))

    def test_is_valid_content_list_returns_false(self):
        with mock.patch(self.mocked_service, return_value=self.invalid_mock):
            self.assertFalse(self.service.is_valid_content_list([9999]))

    def test_get_content_from_service_returns_content(self):
        with mock.patch(self.mocked_service, return_value=self.valid_mock):
            self.assertIsNotNone(self.service.get_content_from_service(1))

    def test_get_content_list_returns_list(self):
        with mock.patch(self.mocked_service, return_value=self.valid_mock):
            self.assertIsInstance(self.service.get_content_list([1]), list)

    def test_get_content_list_returns_empty_list(self):
        with mock.patch(self.mocked_service, return_value=self.invalid_mock):
            return_value = self.service.get_content_list([9999])
            self.assertIsInstance(return_value, list)
            self.assertEqual(return_value, [])