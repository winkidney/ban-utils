import time

from ban_utils import store


def test_redis_counter(counter: store.RedisCounterBackend):
    uid = "test_id"
    assert counter.get(uid) == 0
    counter.increment(uid, 1, 1)
    assert counter.get(uid) == 1
    time.sleep(1)
    assert counter.get(uid) == 0
