from unittest import mock

from ban_utils.contrib import rate_limit


def test_should_too_many2ban_works_with_count(counter):

    ban_callback = mock.Mock()

    @rate_limit.too_many2ban(
        key_fn=lambda: "hello",
        ban_callback=ban_callback,
        counter=counter,
        max_count2ban=2,
        enabled=True,
    )
    def fn_to_test():
        return "hello"

    fn_to_test()
    assert ban_callback.called is False
    fn_to_test()
    assert ban_callback.called is False
    fn_to_test()
    assert ban_callback.called is True


def test_should_too_many2ban_did_not_work_while_disable(counter):

    ban_callback = mock.Mock()

    @rate_limit.too_many2ban(
        key_fn=lambda: "hello",
        ban_callback=ban_callback,
        counter=counter,
        max_count2ban=2,
        enabled=False,
    )
    def fn_to_test():
        return "hello"

    for _ in range(100):
        assert fn_to_test() == "hello"
    assert ban_callback.called is False
