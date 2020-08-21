from abc import ABCMeta, abstractmethod

from redis import Redis


class CounterABC(metaclass=ABCMeta):
    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def get(self, unique_id) -> int:
        pass

    @abstractmethod
    def increment(self, unique_id, number, ttl) -> int:
        pass

    @abstractmethod
    def delete(self, unique_id) -> None:
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


class RedisCounterBackend(CounterABC, RedisMixin):
    def __init__(self, save_prefix: str, redis_client: Redis):
        """
        :type redis_client: redis.Redis
        """
        self._prefix = save_prefix + "_counter"
        self._client = redis_client

    def reset(self):
        self._reset_all()

    def get(self, unique_id) -> int:
        key = self._get_key(unique_id)
        count = self._client.get(
            key
        )
        if count is None:
            return 0
        return int(count)

    def increment(self, unique_id, number, ttl) -> int:
        key = self._get_key(unique_id)
        if self._client.get(key) is None:
            self._client.set(key, 0, ex=ttl)
        for x in range(number):
            self._client.incr(key)
        return self.get(unique_id)

    def delete(self, unique_id) -> None:
        key = self._get_key(unique_id)
        self._client.delete(key)
