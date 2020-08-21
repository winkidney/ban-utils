import pytest

from ban_utils import store


@pytest.fixture()
def redis_cli():
    from redis import Redis
    r = Redis()
    return r


@pytest.fixture()
def counter(request, redis_cli):
    backend = store.RedisCounterBackend("test_me", redis_cli)

    def finalizer():
        backend.reset()

    request.addfinalizer(finalizer)
    return backend
