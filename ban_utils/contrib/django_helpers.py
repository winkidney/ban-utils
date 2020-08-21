import logging

from django.conf import settings
from django.http import HttpRequest


_USE_X_FORWARD_FOR = getattr(settings, 'BANISH_UTILS_USE_HTTP_X_FORWARDED_FOR', True)


def get_ip(request: HttpRequest, *args, **kwargs):
    ip = request.META['REMOTE_ADDR']
    if _USE_X_FORWARD_FOR or not ip or ip == '127.0.0.1':
        ip = request.META.get('HTTP_X_FORWARDED_FOR', ip).split(',')[0].strip()
    if getattr(settings, 'DEBUG', False):
        msg = "banish-utils got remote ip %s" % ip
        logging.debug(msg)
    return ip
