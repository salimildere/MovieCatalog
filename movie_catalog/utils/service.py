import logging

import requests
from django.conf import settings
from django.core.cache import cache
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)


class ContentService:
    service_url = settings.CONTENT_SERVICE_URL
    single_invalid_content_exc_msg = "Content id: {} does not exist"
    invalid_data_content_exc_msg = "Content List must be type list"

    def get_content_from_service(self, content_id):
        url = f"{self.service_url}/api/v1/content/"
        try:
            response = requests.get(url, params={"id": content_id})
        except ConnectionError as exc:
            raise f"Error connecting to content service: {exc}. Content ID: {content_id}"

        content = response.json()
        return content

    def get_content(self, content_id):
        cache_key = f"content_{content_id}"
        if cached_value := cache.get(cache_key):
            return cached_value

        content = self.get_content_from_service(content_id)
        if content["count"] == 0:
            return None

        content = content["results"][0]
        cache.set(cache_key, content, timeout=60 * 60 * 2)
        return content

    def get_content_list(self, content_list):
        content_list_data = []
        for content_id in content_list:
            try:
                content = self.get_content(content_id)
            except Exception as exc:
                logger.error(exc)
                continue

            if content:
                content_list_data.append(content)
        return content_list_data

    def is_valid_content_list(self, content_list, raise_exception=False):
        if type(content_list) is not list:
            raise Exception(self.single_invalid_content_exc_msg.format(content_list))

        for content_id in content_list:
            content = self.get_content(content_id)

            if not content:
                if raise_exception:
                    raise Exception(
                        self.single_invalid_content_exc_msg.format(content_id)
                    )
                else:
                    return False
        return True
