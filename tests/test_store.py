import time

import pytest

from banish_utils import store


@pytest.fixture()
def redis_cli():
    from redis import Redis
    r = Redis()
    return r


@pytest.fixture()
def ban(request, redis_cli):
    backend = store.RedisBanBackend("test_me", redis_cli)

    def finalizer():
        backend.reset()

    request.addfinalizer(finalizer)
    return backend


@pytest.fixture()
def counter(request, redis_cli):
    backend = store.RedisCounterBackend("test_me", redis_cli)

    def finalizer():
        backend.reset()

    request.addfinalizer(finalizer)
    return backend


def test_redis_ban(ban: store.RedisBanBackend):
    uid = "test_id"
    ban.ban(uid, 1)
    assert ban.is_banned(uid) is True
    time.sleep(1)
    assert ban.is_banned(uid) is False


def test_redis_counter(counter: store.RedisCounterBackend):
    uid = "test_id"
    assert counter.get(uid) == 0
    counter.increment(uid, 1, 1)
    assert counter.get(uid) == 1
    time.sleep(1)
    assert counter.get(uid) == 0
