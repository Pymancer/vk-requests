# -*- coding: utf-8 -*-
import time
import unittest

import vk_requests

from vk_requests.auth import StoredVKSession
from vk_requests.exceptions import VkAPIError
from vk_requests.settings import (APP_ID, USER_LOGIN, USER_PASSWORD, PHONE_NUMBER)


class VkTestCase(unittest.TestCase):
    STORED_TOKEN = 'invalid_or_expired_token'

    def setUp(self):
        self.vk_api = vk_requests.create_api(lang='ru')

    @staticmethod
    def _create_api(**kwargs):
        return vk_requests.create_api(
            stored_token = VkTestCase.STORED_TOKEN,
            session_cls=StoredVKSession,
            **kwargs
        )

    def test_get_server_time(self):
        time_1 = time.time() - 5
        time_2 = time_1 + 30
        server_time = self.vk_api.getServerTime()
        self.assertTrue(time_1 <= server_time <= time_2)

    def test_get_server_time_via_token_api(self):
        with self.assertRaises(ValueError) as err:
            resp = self._create_api().getServerTime()
            self.assertIsNone(resp)
            self.assertIn('must be given', str(err))

    def test_get_profiles_via_token(self):
        profiles = self.vk_api.users.get(user_id=1)
        self.assertEqual(profiles[0]['last_name'], u'Дуров')

    def test_users_search(self):
        request_opts = dict(
            city=2,
            age_from=18,
            age_to=50,
            offset=0,
            count=1000,
            fields=['screen_name'])

        # Expect api error because search method requires access token
        with self.assertRaises(VkAPIError) as err:
            resp = self.vk_api.users.search(**request_opts)
            self.assertIsNone(resp)
            self.assertIn('no access_token passed', str(err))

    def test_get_friends(self):
        items = self.vk_api.friends.get(
            fields=['nickname', 'city', 'can_see_all_posts'],
            user_id=1)
        self.assertIsInstance(items, dict)
        friends = items['items']
        for item in friends:
            if 'deactivated' in item:
                # skip deactivated users, they don't have extra fields
                continue
            self.assertIsInstance(item, dict)

            # User can hide this field
            # self.assertIn('city', item)
            self.assertIn('nickname', item)
            self.assertIn('id', item)
            self.assertIn('can_see_all_posts', item)


class VkEmptyTokenTestCase(unittest.TestCase):
    STORED_TOKEN = ''

    def setUp(self):
        self.vk_api = vk_requests.create_api(lang='ru')

    @staticmethod
    def _create_api(**kwargs):
        return vk_requests.create_api(
            stored_token = VkTestCase.STORED_TOKEN,
            session_cls=StoredVKSession,
            **kwargs
        )

    def test_get_server_time(self):
        time_1 = time.time() - 5
        time_2 = time_1 + 30
        server_time = self.vk_api.getServerTime()
        self.assertTrue(time_1 <= server_time <= time_2)

    def test_get_server_time_via_token_api(self):
        with self.assertRaises(ValueError) as err:
            resp = self._create_api().getServerTime()
            self.assertIsNone(resp)
            self.assertIn('must be given', str(err))

    def test_get_profiles_via_token(self):
        profiles = self.vk_api.users.get(user_id=1)
        self.assertEqual(profiles[0]['last_name'], u'Дуров')

    def test_users_search(self):
        request_opts = dict(
            city=2,
            age_from=18,
            age_to=50,
            offset=0,
            count=1000,
            fields=['screen_name'])

        # Expect api error because search method requires access token
        with self.assertRaises(VkAPIError) as err:
            resp = self.vk_api.users.search(**request_opts)
            self.assertIsNone(resp)
            self.assertIn('no access_token passed', str(err))

    def test_get_friends(self):
        items = self.vk_api.friends.get(
            fields=['nickname', 'city', 'can_see_all_posts'],
            user_id=1)
        self.assertIsInstance(items, dict)
        friends = items['items']
        for item in friends:
            if 'deactivated' in item:
                # skip deactivated users, they don't have extra fields
                continue
            self.assertIsInstance(item, dict)

            # User can hide this field
            # self.assertIn('city', item)
            self.assertIn('nickname', item)
            self.assertIn('id', item)
            self.assertIn('can_see_all_posts', item)