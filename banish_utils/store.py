from abc import ABCMeta, abstractmethod

from redis import Redis


class BanBackendABC(metaclass=ABCMeta):

    @abstractmethod
    def reset(self):
        """
        clear all banned target
        """
        pass

    @abstractmethod
    def ban(self, unique_id: str, ttl: int, meta=None):
        pass

    @abstractmethod
    def unban(self, unique_id: str):
        pass

    @abstractmethod
    def is_banned(self, unique_id):
        pass


class CounterABC(metaclass=ABCMeta):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get(self, unique_id):
        pass

    @abstractmethod
    def increment(self, unique_id, number, ttl):
        pass

    @abstractmethod
    def delete(self, unique_id):
        pass


class RedisMixin:
    def _get_key(self, unique_id):
        return f"{self._prefix}_{unique_id}"

    def _keys(self):
        return tuple(self._client.keys(f"{self._prefix}*"))

    def _reset_all(self):
        keys = self._keys()
        if len(keys) <= 0:
            return
        self._client.delete(*keys)


class RedisBanBackend(BanBackendABC, RedisMixin):
    def __init__(self, save_prefix: str, redis_client: Redis):
        self._prefix = save_prefix + "_ban"
        self._client = redis_client

    def reset(self):
        self._reset_all()

    def ban(self, unique_id: str, ttl: int, meta: str = None):
        if meta is None:
            meta = ""
        key = self._get_key(unique_id)
        return self._client.set(key, meta, ex=ttl)

    def is_banned(self, unique_id):
        key = self._get_key(unique_id)
        return self._client.get(key) is not None

    def unban(self, unique_id: str):
        key = self._get_key(unique_id)
        return self._client.delete(key)


class RedisCounterBackend(CounterABC, RedisMixin):
    def __init__(self, save_prefix: str, redis_client: Redis):
        """
        :type redis_client: redis.Redis
        """
        self._prefix = save_prefix + "_counter"
        self._client = redis_client

    def reset(self):
        self._reset_all()

    def get(self, unique_id):
        key = self._get_key(unique_id)
        count = self._client.get(
            key
        )
        if count is None:
            return 0
        return int(count)

    def increment(self, unique_id, number, ttl):
        key = self._get_key(unique_id)
        if self._client.get(key) is None:
            self._client.set(key, 0, ex=ttl)
        for x in range(number):
            self._client.incr(key)

    def delete(self, unique_id):
        key = self._get_key(unique_id)
        self._client.delete(key)
