from functools import wraps

from banish_utils.store import CounterABC, BanBackendABC


def too_many2ban(
        key_fn: callable,
        ban_callback: callable,
        counter: CounterABC, banner: BanBackendABC,
        max_count2ban=10,
        counter_ttl=60 * 5,
        ban_ttl=60 * 5,
):
    _counter = counter
    _banner = banner

    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            key = key_fn(*args, **kwargs)
            if _banner.is_banned(key):
                return ban_callback(*args, **kwargs)
            count = _counter.get(key)
            if count >= max_count2ban:
                _banner.ban(key, ttl=ban_ttl)
            counter.increment(key, 1, counter_ttl)
            return fn(*args, **kwargs)
        return wrapped

    return wrapper
