import logging

from django.core.cache import cache

logger = logging.getLogger(__name__)


class CacheClient(object):

    def __init__(self):
        self.cache = cache

    @staticmethod
    def _get_cache_key(key, namespace):
        if not namespace:
            return key
        return '{}:{}'.format(namespace, key)

    def get(self, key, default=None, namespace=None):
        cache_key = self._get_cache_key(key, namespace)

        try:
            response = self.cache.get(cache_key, default)
        except Exception as e:
            logger.warning('Failed to get the cache', str(e))
            return default

        return response

    def set(self, key, value, timeout=None, namespace=None):
        cache_key = self._get_cache_key(key, namespace)

        try:
            self.cache.set(cache_key, value, timeout)
        except Exception as e:
            logger.warning('Failed to set the key to cache', str(e))
            return None

    def delete(self, key, namespace=None):
        cache_key = self._get_cache_key(key, namespace)

        try:
            self.cache.delete(cache_key)
        except Exception as e:
            logger.warning('Failed to delete the key to cache', str(e))
            return None


cache_client = CacheClient()
