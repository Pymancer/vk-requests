# -*- coding: utf-8 -*-
import time
import unittest

import vk_requests

from vk_requests.auth import StoredVKSession
from vk_requests.exceptions import VkAPIError
from vk_requests.settings import (APP_ID, USER_LOGIN, USER_PASSWORD, PHONE_NUMBER)


class VkTestCase(unittest.TestCase):
    STORED_TOKEN = vk_requests.create_api(app_id=APP_ID,
                                          login=USER_LOGIN,
                                          password=USER_PASSWORD,
                                          phone_number=PHONE_NUMBER,
                                          scope=['offline', 'messages', 'status'])._session.access_token

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
        time_2 = time_1 + 10
        server_time = self.vk_api.getServerTime()
        self.assertTrue(time_1 <= server_time <= time_2)

    def test_get_server_time_via_token_api(self):
        time_1 = time.time() - 5
        time_2 = time_1 + 20
        server_time = self._create_api().getServerTime()
        self.assertTrue(time_1 <= server_time <= time_2)

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

        # Create token-based API
        api = self._create_api()
        resp = api.users.search(**request_opts)
        self.assertIsInstance(resp, dict)
        total_num, items = resp['count'], resp['items']
        self.assertIsInstance(total_num, int)
        for item in items:
            self.assertIsInstance(item, dict)
            self.assertIn('screen_name', item)

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

    def test_set_status(self):
        """Test requires scope='status' vk permissions
        """
        status_text = 'Welcome to noagent.168.estate'
        api = self._create_api(scope=['offline', 'messages', 'status'])
        self.assertEqual(api._session.auth_api.scope, ['offline', 'messages', 'status'])

        # Set the status
        resp = api.status.set(text=status_text)
        self.assertEqual(resp, 1)

        # Check the status
        resp = api.status.get()
        self.assertEqual(resp, {'text': status_text})

    def test_multi_scope_requests(self):
        api = self._create_api(scope=['messages', 'status'])
        resp = api.status.get()
        self.assertIn('text', resp)

        resp = api.messages.get()
        self.assertIsInstance(resp, dict)
        total_msg, msg_list = resp['count'], resp['items']
        self.assertIsInstance(total_msg, int)
        for msg in msg_list:
            self.assertIsInstance(msg, dict)

    def test_likes_get_list(self):
        api = self._create_api()
        resp = api.likes.getList(type='post', owner_id=1, item_id=815649)
        self.assertIn('count', resp)
        self.assertIn('items', resp)
        for user_id in resp['items']:
            self.assertIsInstance(user_id, int)
