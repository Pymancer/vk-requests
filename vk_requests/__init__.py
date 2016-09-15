
from vk_requests.auth import (InteractiveVKSession, VKSession, StoredVKSession, CaptchaVKSession)
from vk_requests.api import API


__version__ = '0.9.6'


def create_api(app_id=None, login=None, password=None, phone_number=None,
               timeout=10, scope='offline', api_version=None,
               session_cls=VKSession, stored_token=None, **method_default_args):
    """Factory method to explicitly create API with app_id, login, password
    and phone_number parameters.

    If the app_id, login, password are not passed, then token-free session
    will be created automatically

    :param app_id: int: vk application id, more info: https://vk.com/dev/main
    :param login: str: vk login
    :param password: str: vk password
    :param phone_number: str: phone number with country code (+71234568990)
    :param timeout: int: api timeout in seconds
    :param scope: str or list of str: vk session scope
    :param api_version: str: vk api version
    :param session_cls: VKSession: session implementation class
    :param method_default_args: api kwargs
    :return: api instance
    :rtype : vk_requests.api.API

    Passing StoredVKSession as vk session class with an active token
    could speed up the initial connection process, which is
    especially helpful when the callee could use many independent
    sessions in a relatively short period of time (1 day) and
    using singleton class for storing api instance is not an available option.

    If there is any possibility that provided token invalid, expired
    or could expire during session activity it would be much
    safer to provide app_id, login and password as well
    otherwise api will fail with ValueError.

    All changes were made with a primary intention to not to break existing code.
    example call:
    from vk_requests import StoredVKSession
    api = vk_requests.create_api(app_id=app_id, login=login, password=password,
                                 stored_token=token, session_cls=StoredVKSession)
    Important: stored token should have same scope as callee passing to api factory
    :param stored_token: str: previously obtained, preferably valid token

    helper class to avoid manual login/password entering passing captcha security check:
    from vk_requests import CaptchaVKSession
    api = vk_requests.create_api(app_id=app_id, login=login, password=password,
                                 session_cls=CaptchaVKSession)
    """
    session = session_cls(app_id, login, password, phone_number=phone_number,
                          scope=scope, api_version=api_version, stored_token=stored_token)
    return API(session=session, timeout=timeout, **method_default_args)