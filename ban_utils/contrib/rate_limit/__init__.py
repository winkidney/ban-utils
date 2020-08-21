from functools import wraps

from ban_utils.store import CounterABC


def too_many2ban(
        key_fn: callable,
        ban_callback: callable,
        counter: CounterABC,
        max_count2ban=10,
        counter_ttl=60 * 5,
        enabled=True,
):
    _counter = counter

    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not enabled:
                return fn(*args, **kwargs)
            key = key_fn(*args, **kwargs)
            count = _counter.get(key)
            if count >= max_count2ban:
                return ban_callback(*args, **kwargs)
            counter.increment(key, 1, counter_ttl)
            return fn(*args, **kwargs)
        return wrapped

    return wrapper
