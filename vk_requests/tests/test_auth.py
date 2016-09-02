# -*- coding: utf-8 -*-
import unittest

import six

import vk_requests

from vk_requests import settings
from vk_requests.auth import AuthAPI, VKSession, StoredVKSession, StoredAuthAPI


class VKSessionTest(unittest.TestCase):
    @staticmethod
    def get_default_vk_session(**kwargs):
        return VKSession(app_id=settings.APP_ID,
                         user_login=settings.USER_LOGIN,
                         user_password=settings.USER_PASSWORD,
                         phone_number=settings.PHONE_NUMBER, **kwargs)

    def test_session_init(self):
        session = self.get_default_vk_session()
        # Expect no errors
        self.assertIsInstance(session, VKSession)

        # Token is required, cuz auth params are being passed
        self.assertTrue(session.auth_api.is_token_required)

    def test_custom_auth_api_cls(self):
        class MyAuthAPI(AuthAPI):
            @staticmethod
            def get_captcha_key(captcha_image_url):
                return 1

        # Create session with custom AuthAPI implementation
        session = self.get_default_vk_session(auth_api_cls=MyAuthAPI)
        self.assertIsInstance(session.auth_api, MyAuthAPI)

    def test_access_token_property(self):
        # Check token getter
        session = self.get_default_vk_session()
        self.assertTrue(session.access_token)
        self.assertIsInstance(session.access_token, six.string_types)

        # Check token setter
        new_token_value = 'my_fake_access_token'
        session.access_token = new_token_value
        self.assertEqual(session.access_token, new_token_value)
        self.assertEqual(session.censored_access_token, 'my_f***oken')


class StoredVKSessionTest(unittest.TestCase):
    STORED_TOKEN = vk_requests.create_api(app_id=settings.APP_ID,
                                          login=settings.USER_LOGIN,
                                          password=settings.USER_PASSWORD,
                                          phone_number=settings.PHONE_NUMBER)._session.access_token

    @staticmethod
    def get_default_vk_session(**kwargs):
        return StoredVKSession(app_id=settings.APP_ID,
                               user_login=settings.USER_LOGIN,
                               user_password=settings.USER_PASSWORD,
                               phone_number=settings.PHONE_NUMBER,
                               stored_token=StoredVKSessionTest.STORED_TOKEN,
                               **kwargs)

    def test_session_init(self):
        session = self.get_default_vk_session()
        # Expect no errors
        self.assertIsInstance(session, VKSession)
        self.assertIsInstance(session, StoredVKSession)

        # Token is required, cuz auth stored token passed
        self.assertTrue(session.auth_api.is_token_required)

    def test_custom_auth_api_cls(self):
        class MyAuthAPI(StoredAuthAPI):
            @staticmethod
            def get_captcha_key(captcha_image_url):
                return 1

        # Create session with custom AuthAPI implementation
        session = self.get_default_vk_session(auth_api_cls=MyAuthAPI)
        self.assertIsInstance(session.auth_api, MyAuthAPI)

    def test_access_token_property(self):
        # Check token getter
        session = self.get_default_vk_session()
        self.assertTrue(session.access_token)
        self.assertIsInstance(session.access_token, six.string_types)
        self.assertEqual(session.access_token, self.STORED_TOKEN)

        # Check token setter
        new_token_value = 'my_fake_access_token'
        session.access_token = new_token_value
        self.assertEqual(session.access_token, new_token_value)
        self.assertEqual(session.censored_access_token, 'my_f***oken')


class ExpiredStoredVKSessionTest(unittest.TestCase):
    STORED_TOKEN = '40a9ceff5ce6f56522973c873a0233d654d4f5ab6162eddd61850c24179fae7243b9725274ce38b71397d'

    @staticmethod
    def get_default_vk_session(**kwargs):
        return StoredVKSession(app_id=settings.APP_ID,
                               user_login=settings.USER_LOGIN,
                               user_password=settings.USER_PASSWORD,
                               phone_number=settings.PHONE_NUMBER,
                               stored_token=ExpiredStoredVKSessionTest.STORED_TOKEN,
                               **kwargs)

    def test_session_init(self):
        session = self.get_default_vk_session()
        # Expect no errors
        self.assertIsInstance(session, VKSession)
        self.assertIsInstance(session, StoredVKSession)

        # Token is required, cuz auth stored token passed
        self.assertTrue(session.auth_api.is_token_required)

    def test_custom_auth_api_cls(self):
        class MyAuthAPI(StoredAuthAPI):
            @staticmethod
            def get_captcha_key(captcha_image_url):
                return 1

        # Create session with custom AuthAPI implementation
        session = self.get_default_vk_session(auth_api_cls=MyAuthAPI)
        self.assertIsInstance(session.auth_api, MyAuthAPI)

    def test_access_token_property(self):
        # Check token getter
        session = self.get_default_vk_session()
        self.assertTrue(session.access_token)
        self.assertIsInstance(session.access_token, six.string_types)
        self.assertEqual(session.access_token, self.STORED_TOKEN)

        # Check token setter
        new_token_value = 'my_fake_access_token'
        session.access_token = new_token_value
        self.assertEqual(session.access_token, new_token_value)
        self.assertEqual(session.censored_access_token, 'my_f***oken')


class InvalidStoredVKSessionTest(unittest.TestCase):
    STORED_TOKEN = 'invalid_token'

    @staticmethod
    def get_default_vk_session(**kwargs):
        return StoredVKSession(app_id=settings.APP_ID,
                               user_login=settings.USER_LOGIN,
                               user_password=settings.USER_PASSWORD,
                               phone_number=settings.PHONE_NUMBER,
                               stored_token=InvalidStoredVKSessionTest.STORED_TOKEN,
                               **kwargs)

    def test_session_init(self):
        session = self.get_default_vk_session()
        # Expect no errors
        self.assertIsInstance(session, VKSession)
        self.assertIsInstance(session, StoredVKSession)

        # Token is required, cuz auth stored token passed
        self.assertTrue(session.auth_api.is_token_required)

    def test_custom_auth_api_cls(self):
        class MyAuthAPI(StoredAuthAPI):
            @staticmethod
            def get_captcha_key(captcha_image_url):
                return 1

        # Create session with custom AuthAPI implementation
        session = self.get_default_vk_session(auth_api_cls=MyAuthAPI)
        self.assertIsInstance(session.auth_api, MyAuthAPI)

    def test_access_token_property(self):
        # Check token getter
        session = self.get_default_vk_session()
        self.assertTrue(session.access_token)
        self.assertIsInstance(session.access_token, six.string_types)
        self.assertEqual(session.access_token, self.STORED_TOKEN)

        # Check token setter
        new_token_value = 'my_fake_access_token'
        session.access_token = new_token_value
        self.assertEqual(session.access_token, new_token_value)
        self.assertEqual(session.censored_access_token, 'my_f***oken')


class EmptyStoredVKSessionTest(unittest.TestCase):
    STORED_TOKEN = vk_requests.create_api(app_id=settings.APP_ID,
                                          login=settings.USER_LOGIN,
                                          password=settings.USER_PASSWORD,
                                          phone_number=settings.PHONE_NUMBER)._session.access_token

    @staticmethod
    def get_default_vk_session(**kwargs):
        return StoredVKSession(stored_token=EmptyStoredVKSessionTest.STORED_TOKEN, **kwargs)

    def test_session_init(self):
        session = self.get_default_vk_session()
        # Expect no errors
        self.assertIsInstance(session, VKSession)
        self.assertIsInstance(session, StoredVKSession)

        # Token is required, cuz auth stored token passed
        self.assertTrue(session.auth_api.is_token_required)

    def test_custom_auth_api_cls(self):
        class MyAuthAPI(StoredAuthAPI):
            @staticmethod
            def get_captcha_key(captcha_image_url):
                return 1

        # Create session with custom AuthAPI implementation
        session = self.get_default_vk_session(auth_api_cls=MyAuthAPI)
        self.assertIsInstance(session.auth_api, MyAuthAPI)

    def test_access_token_property(self):
        # Check token getter
        session = self.get_default_vk_session()
        self.assertTrue(session.access_token)
        self.assertIsInstance(session.access_token, six.string_types)
        self.assertEqual(session.access_token, self.STORED_TOKEN)

        # Check token setter
        new_token_value = 'my_fake_access_token'
        session.access_token = new_token_value
        self.assertEqual(session.access_token, new_token_value)
        self.assertEqual(session.censored_access_token, 'my_f***oken')