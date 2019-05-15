import unittest
import uuid

from rocketchat_API.APIExceptions.RocketExceptions import RocketAuthenticationException, RocketMissingParamException
from rocketchat_API.rocketchat import RocketChat


class TestServer(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)

    def test_info(self):
        info = self.rocket.info().json()
        self.assertTrue('info' in info)
        self.assertTrue(info.get('success'))

    def test_statistics(self):
        statistics = self.rocket.statistics().json()
        self.assertTrue(statistics.get('success'))

    def test_statistics_list(self):
        statistics_list = self.rocket.statistics_list().json()
        self.assertTrue(statistics_list.get('success'))

    def test_directory(self):
        directory = self.rocket.directory(
            query={'text': 'rocket', 'type': 'users'}).json()
        self.assertTrue(directory.get('success'))

    def test_spotlight(self):
        spotlight = self.rocket.spotlight(query='user1').json()
        self.assertTrue(spotlight.get('success'))
        self.assertIsNotNone(spotlight.get('users'), 'No users list found')
        self.assertIsNotNone(spotlight.get('rooms'), 'No rooms list found')


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)
        user2_exists = self.rocket.users_info(
            username='user2').json().get('success')
        if user2_exists:
            user_id = self.rocket.users_info(
                username='user2').json().get('user').get('_id')
            self.rocket.users_delete(user_id)

    def test_login(self):
        login = self.rocket.login(self.user, self.password).json()

        with self.assertRaises(RocketAuthenticationException):
            self.rocket.login(self.user, 'bad_password')

        self.assertEqual(login.get('status'), 'success')
        self.assertTrue('authToken' in login.get('data'))
        self.assertTrue('userId' in login.get('data'))

    def test_login_email(self):
        login = self.rocket.login(self.email, self.password).json()

        with self.assertRaises(RocketAuthenticationException):
            self.rocket.login(self.user, 'bad_password')

        self.assertEqual(login.get('status'), 'success')
        self.assertTrue('authToken' in login.get('data'))
        self.assertTrue('userId' in login.get('data'))

    def test_me(self):
        me = self.rocket.me().json()
        self.assertTrue(me.get('success'))
        self.assertEqual(me.get('username'), self.user)
        self.assertEqual(me.get('name'), self.user)

    def test_logout(self):
        self.rocket.login(self.user, self.password).json()
        logout = self.rocket.logout().json()
        self.assertEqual(logout.get('status'), 'success')

    def test_users_info(self):
        login = self.rocket.login(self.user, self.password).json()
        user_id = login.get('data').get('userId')

        users_info_by_id = self.rocket.users_info(user_id=user_id).json()
        self.assertTrue(users_info_by_id.get('success'))
        self.assertEqual(users_info_by_id.get('user').get('_id'), user_id)

        users_info_by_name = self.rocket.users_info(username=self.user).json()
        self.assertTrue(users_info_by_name.get('success'))
        self.assertEqual(users_info_by_name.get('user').get('name'), self.user)

        with self.assertRaises(RocketMissingParamException):
            self.rocket.users_info()

    def test_users_get_presence(self):
        login = self.rocket.login(self.user, self.password).json()
        users_get_presence = self.rocket.users_get_presence(
            user_id=login.get('data').get('userId')).json()
        self.assertTrue(users_get_presence.get('success'))

        users_get_presence_by_name = self.rocket.users_get_presence(
            username=self.user).json()
        self.assertTrue(users_get_presence_by_name.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.users_get_presence()

    def test_users_get_avatar(self):
        login = self.rocket.login(self.user, self.password).json()

        users_get_avatar = self.rocket.users_get_avatar(user_id='no_user')
        self.assertEqual(users_get_avatar.status_code, 400)

        users_get_avatar = self.rocket.users_get_avatar(
            user_id=login.get('data').get('userId'))
        self.assertGreater(len(users_get_avatar.text), 0)

        users_get_avatar = self.rocket.users_get_avatar(username=self.user)
        self.assertGreater(len(users_get_avatar.text), 0)

        with self.assertRaises(RocketMissingParamException):
            self.rocket.users_get_avatar()

    def test_users_reset_avatar(self):
        login = self.rocket.login(self.user, self.password).json()
        users_reset_avatar = self.rocket.users_reset_avatar(
            user_id=login.get('data').get('userId')).json()
        self.assertTrue(users_reset_avatar.get('success'))

        users_reset_avatar = self.rocket.users_reset_avatar(
            username=self.user).json()
        self.assertTrue(users_reset_avatar.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.users_reset_avatar()

    def test_users_create_token(self):
        login = self.rocket.login(self.user, self.password).json()
        users_create_token = self.rocket.users_create_token(
            user_id=login.get('data').get('userId')).json()
        self.assertTrue(users_create_token.get('success'))
        self.assertIn('authToken', users_create_token.get('data'))
        self.assertIn('userId', users_create_token.get('data'))

        users_create_token = self.rocket.users_create_token(
            username=login.get('data').get('me').get('name')).json()
        self.assertTrue(users_create_token.get('success'))
        self.assertIn('authToken', users_create_token.get('data'))
        self.assertIn('userId', users_create_token.get('data'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.users_create_token()

    def test_users_create_update_delete(self):
        users_create = self.rocket.users_create(email='email2@domain.com', name='user2', password=self.password,
                                                username='user2').json()
        self.assertTrue(users_create.get('success'), users_create.get('error'))

        user_id = users_create.get('user').get('_id')
        users_update = self.rocket.users_update(user_id, email='anewemailhere@domain.com', name='newname',
                                                password=self.password, username='newusername').json()
        self.assertTrue(users_update.get('success'), 'Can not update user')
        self.assertEqual(users_update.get('user').get(
            'emails')[0].get('address'), 'anewemailhere@domain.com')
        self.assertEqual(users_update.get('user').get('name'), 'newname')

        # ToDo: For some reason update is not updating the username
        # self.assertEqual(users_update.get(
        #     'user').get('username'), 'newusername')

        users_delete = self.rocket.users_delete(user_id).json()
        self.assertTrue(users_delete.get('success'))

    def test_users_set_avatar_from_file(self):
        users_set_avatar = self.rocket.users_set_avatar(
            avatar_url='tests/avatar.png').json()
        self.assertTrue(users_set_avatar.get('success'),
                        users_set_avatar.get('error'))

    def test_users_set_avatar_from_url(self):
        # ToDo: Modify this test so it can run while offline
        users_set_avatar = self.rocket.users_set_avatar(
            avatar_url='https://api.adorable.io/avatars/285/rocket.face.png').json()
        self.assertTrue(users_set_avatar.get('success'),
                        users_set_avatar.get('error'))

    def test_users_forgot_password(self):
        users_forgot_password = self.rocket.users_forgot_password(
            email='email@domain.com').json()
        self.assertTrue(users_forgot_password.get('success'))

    def test_users_set_get_preferences(self):
        users_set_preferences = self.rocket.users_set_preferences(user_id=self.rocket.me().json().get('_id'),
                                                                  data={'useEmojis': False}).json()
        self.assertTrue(users_set_preferences.get('success'))
        users_get_preferences = self.rocket.users_get_preferences().json()
        self.assertTrue(users_get_preferences.get('success'))

    def test_users_list(self):
        users_list = self.rocket.users_list().json()
        self.assertTrue(users_list.get('success'))


class TestChat(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)

    def test_chat_post_update_delete_message(self):
        chat_post_message = self.rocket.chat_post_message(
            "hello", channel='GENERAL').json()
        self.assertEqual(chat_post_message.get('channel'), 'GENERAL')
        self.assertEqual(chat_post_message.get('message').get('msg'), 'hello')
        self.assertTrue(chat_post_message.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.chat_post_message(text='text')

        msg_id = chat_post_message.get('message').get('_id')
        chat_get_message = self.rocket.chat_get_message(msg_id=msg_id).json()
        self.assertEqual(chat_get_message.get('message').get('_id'), msg_id)

        chat_update = self.rocket.chat_update(room_id=chat_post_message.get('channel'),
                                              msg_id=chat_post_message.get(
                                                  'message').get('_id'),
                                              text='hello again').json()

        self.assertEqual(chat_update.get('message').get('msg'), 'hello again')
        self.assertTrue(chat_update.get('success'))

        chat_delete = self.rocket.chat_delete(room_id=chat_post_message.get('channel'),
                                              msg_id=chat_post_message.get('message').get('_id')).json()
        self.assertTrue(chat_delete.get('success'))

    def test_chat_post_react(self):
        message_id = self.rocket.chat_post_message(
            "hello", channel='GENERAL').json().get('message').get('_id')
        chat_react = self.rocket.chat_react(msg_id=message_id).json()
        self.assertTrue(chat_react.get('success'))

    def test_post_pin_unpin(self):
        message_id = self.rocket.chat_post_message(
            "hello", channel='GENERAL').json().get('message').get('_id')
        chat_pin_message = self.rocket.chat_pin_message(message_id).json()
        self.assertTrue(chat_pin_message.get('success'))
        self.assertEqual(chat_pin_message.get(
            'message').get('t'), 'message_pinned')

        chat_unpin_message = self.rocket.chat_unpin_message(message_id).json()
        self.assertTrue(chat_unpin_message.get('success'))

    def test_post_star_unstar(self):
        message_id = self.rocket.chat_post_message(
            "hello", channel='GENERAL').json().get('message').get('_id')
        chat_star_message = self.rocket.chat_star_message(message_id).json()
        self.assertTrue(chat_star_message.get('success'))

        chat_unstar_message = self.rocket.chat_unstar_message(
            message_id).json()
        self.assertTrue(chat_unstar_message.get('success'))

    def test_chat_search(self):
        chat_search = self.rocket.chat_search(
            room_id='GENERAL', search_text='hello').json()
        self.assertTrue(chat_search.get('success'))

    def test_chat_get_message_read_receipts(self):
        message_id = self.rocket.chat_post_message(
            "hello", channel='GENERAL').json().get('message').get('_id')
        chat_get_message_read_receipts = self.rocket.chat_get_message_read_receipts(
            message_id=message_id).json()
        self.assertTrue(chat_get_message_read_receipts.get('success'))
        self.assertIn('receipts', chat_get_message_read_receipts)


class TestChannels(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket.channels_add_owner('GENERAL', username=self.user)
        self.rocket = RocketChat(self.user, self.password)

        testuser = self.rocket.users_info(username='testuser1').json()
        if not testuser.get('success'):
            testuser = self.rocket.users_create(
                'testuser1@domain.com', 'testuser1', 'password', 'testuser1').json()
            if not testuser.get('success'):
                self.fail("can't create test user")

        self.testuser_id = testuser.get('user').get('_id')

    def tearDown(self):
        self.rocket.users_delete(self.testuser_id)

    def test_channels_list(self):
        channels_list = self.rocket.channels_list().json()
        self.assertTrue(channels_list.get('success'))
        self.assertIn('channels', channels_list)

    def test_channels_list_joined(self):
        channels_list_joined = self.rocket.channels_list_joined().json()
        self.assertTrue(channels_list_joined.get('success'))
        self.assertIn('channels', channels_list_joined)

    def test_channels_info(self):
        channels_info = self.rocket.channels_info(room_id='GENERAL').json()
        self.assertTrue(channels_info.get('success'))
        self.assertIn('channel', channels_info)
        self.assertEqual(channels_info.get('channel').get('_id'), 'GENERAL')
        channel_name = channels_info.get('channel').get('name')
        channels_info = self.rocket.channels_info(channel=channel_name).json()
        self.assertTrue(channels_info.get('success'))
        self.assertIn('channel', channels_info)
        self.assertEqual(channels_info.get('channel').get('_id'), 'GENERAL')
        self.assertEqual(channels_info.get(
            'channel').get('name'), channel_name)

        with self.assertRaises(RocketMissingParamException):
            self.rocket.channels_info()

    def test_channels_history(self):
        channels_history = self.rocket.channels_history(
            room_id='GENERAL').json()
        self.assertTrue(channels_history.get('success'))
        self.assertIn('messages', channels_history)

    def test_channels_add_all(self):
        channels_add_all = self.rocket.channels_add_all('GENERAL').json()
        self.assertTrue(channels_add_all.get('success'))

    def test_channels_add_and_remove_moderator(self):
        me = self.rocket.me().json()
        channels_add_moderator = self.rocket.channels_add_moderator(
            'GENERAL', me.get('_id')).json()
        self.assertTrue(channels_add_moderator.get('success'))
        channels_remove_moderator = self.rocket.channels_remove_moderator(
            'GENERAL', me.get('_id')).json()
        self.assertTrue(channels_remove_moderator.get('success'))

    def test_channels_list_moderator(self):
        channels_list_moderator = self.rocket.channels_moderators(
            room_id='GENERAL').json()
        self.assertTrue(channels_list_moderator.get('success'))
        channel_name = self.rocket.channels_info(room_id='GENERAL').json().get("channel").get("name")
        channels_list_moderator_by_name = self.rocket.channels_moderators(
            channel=channel_name).json()
        self.assertTrue(channels_list_moderator_by_name.get('success'))
        with self.assertRaises(RocketMissingParamException):
            self.rocket.channels_moderators()

    def test_channels_add_and_remove_owner(self):
        channels_add_owner = self.rocket.channels_add_owner('GENERAL',
                                                            user_id=self.testuser_id).json()
        self.assertTrue(channels_add_owner.get('success'),
                        channels_add_owner.get('error'))
        another_owner_id = self.rocket.users_info(username='user1').json().get('user').get('_id')
        self.rocket.channels_add_owner('GENERAL', user_id=another_owner_id).json()
        channels_remove_owner = self.rocket.channels_remove_owner('GENERAL',
                                                                  user_id=self.testuser_id).json()
        self.assertTrue(channels_remove_owner.get('success'),
                        channels_remove_owner.get('error'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.channels_add_owner(room_id='GENERAL')

    def test_channels_archive_unarchive(self):
        channels_archive = self.rocket.channels_archive('GENERAL').json()
        self.assertTrue(channels_archive.get('success'))
        channels_unarchive = self.rocket.channels_unarchive('GENERAL').json()
        self.assertTrue(channels_unarchive.get('success'))

    def test_channels_close_open(self):
        channels_close = self.rocket.channels_close('GENERAL').json()
        self.assertTrue(channels_close.get('success'))
        channels_open = self.rocket.channels_open('GENERAL').json()
        self.assertTrue(channels_open.get('success'))

    def test_channels_create_delete(self):
        name = str(uuid.uuid1())
        channels_create = self.rocket.channels_create(name).json()
        self.assertTrue(channels_create.get('success'))
        self.assertEqual(name, channels_create.get('channel').get('name'))
        channels_delete = self.rocket.channels_delete(channel=name).json()
        self.assertTrue(channels_delete.get('success'))
        channels_create = self.rocket.channels_create(name).json()
        self.assertTrue(channels_create.get('success'))
        room_id = channels_create.get('channel').get('_id')
        channels_delete = self.rocket.channels_delete(room_id=room_id).json()
        self.assertTrue(channels_delete.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.channels_delete()

    def test_channels_get_integrations(self):
        channels_get_integrations = self.rocket.channels_get_integrations(
            room_id='GENERAL').json()
        self.assertTrue(channels_get_integrations.get('success'))

    def test_channels_invite(self):
        channels_invite = self.rocket.channels_invite(
            'GENERAL', self.testuser_id).json()
        self.assertTrue(channels_invite.get('success'))

    def test_channels_kick(self):
        channels_kick = self.rocket.channels_kick(
            'GENERAL', self.testuser_id).json()
        self.assertTrue(channels_kick.get('success'))

    def test_channels_leave(self):
        channels_leave = self.rocket.channels_leave('GENERAL').json()
        self.assertFalse(channels_leave.get('success'))
        self.assertEqual(channels_leave.get('errorType'),
                         'error-you-are-last-owner')

        name = str(uuid.uuid1())
        channels_create = self.rocket.channels_create(name).json()
        self.rocket.channels_invite(room_id=channels_create.get('channel').get('_id'),
                                    user_id=self.testuser_id)
        self.rocket.channels_add_owner(channels_create.get('channel').get('_id'),
                                       user_id=self.testuser_id).json()
        channels_leave = self.rocket.channels_leave(
            channels_create.get('channel').get('_id')).json()
        self.assertTrue(channels_leave.get('success'))

    def test_channels_rename(self):
        name = str(uuid.uuid1())
        name2 = str(uuid.uuid1())
        channels_create = self.rocket.channels_create(name).json()
        channels_rename = self.rocket.channels_rename(room_id=channels_create.get('channel').get('_id'),
                                                      name=name2).json()
        self.assertTrue(channels_rename.get('success'))
        self.assertEqual(channels_rename.get('channel').get('name'), name2)

    def test_channels_set_description(self):
        description = str(uuid.uuid1())
        channels_set_description = self.rocket.channels_set_description(
            'GENERAL', description).json()
        self.assertTrue(channels_set_description.get('success'))
        self.assertEqual(channels_set_description.get('description'), description,
                         'Description does not match')

    def test_channels_set_join_code(self):
        join_code = str(uuid.uuid1())
        channels_set_join_code = self.rocket.channels_set_join_code(
            'GENERAL', join_code).json()
        self.assertTrue(channels_set_join_code.get('success'))

    def test_channels_set_read_only(self):
        channels_set_read_only = self.rocket.channels_set_read_only(
            'GENERAL', True).json()
        self.assertTrue(channels_set_read_only.get('success'))
        channels_set_read_only = self.rocket.channels_set_read_only(
            'GENERAL', False).json()
        self.assertTrue(channels_set_read_only.get('success'))

    def test_channels_set_topic(self):
        topic = str(uuid.uuid1())
        channels_set_topic = self.rocket.channels_set_topic(
            'GENERAL', topic).json()
        self.assertTrue(channels_set_topic.get('success'))
        self.assertEqual(channels_set_topic.get('topic'), topic,
                         'Topic does not match')

    def test_channels_set_type(self):
        name = str(uuid.uuid1())
        channels_create = self.rocket.channels_create(name).json()
        self.assertTrue(channels_create.get('success'))

        channels_set_type = self.rocket.channels_set_type(
            channels_create.get('channel').get('_id'), 'p').json()
        self.assertTrue(channels_set_type.get('success'))
        self.assertTrue(channels_set_type.get('channel').get('t'), 'p')

        channels_set_type = self.rocket.channels_set_type(
            channels_create.get('channel').get('_id'), 'c').json()
        # should fail because this is no more a channel
        self.assertFalse(channels_set_type.get('success'))

    def test_channels_set_announcement(self):
        announcement = str(uuid.uuid1())
        channels_set_announcement = self.rocket.channels_set_announcement(
            'GENERAL', announcement).json()
        self.assertTrue(channels_set_announcement.get('success'))
        self.assertEqual(channels_set_announcement.get('announcement'), announcement,
                         'Topic does not match')

    def test_channels_set_custom_fields(self):
        cf = {'key': 'value'}
        channels_set_custom_fields = self.rocket.channels_set_custom_fields(
            'GENERAL', cf).json()
        self.assertTrue(channels_set_custom_fields.get('success'))
        self.assertEqual(
            cf, channels_set_custom_fields['channel']['customFields'])

    def test_channels_members(self):
        channels_members = self.rocket.channels_members(
            room_id='GENERAL').json()
        self.assertTrue(channels_members.get('success'))
        channels_members = self.rocket.channels_members(
            channel='general').json()
        self.assertTrue(channels_members.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.channels_members()

    def test_channels_roles(self):
        channels_roles = self.rocket.channels_roles(room_id='GENERAL').json()
        self.assertTrue(channels_roles.get('success'))
        self.assertIsNotNone(channels_roles.get('roles'))
        channels_roles = self.rocket.channels_roles(room_name='general').json()
        self.assertTrue(channels_roles.get('success'))
        self.assertIsNotNone(channels_roles.get('roles'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.channels_roles()

    def test_channels_files(self):
        channels_files = self.rocket.channels_files(room_id='GENERAL').json()
        self.assertTrue(channels_files.get('success'))

        channels_files = self.rocket.channels_files(room_name='general').json()
        self.assertTrue(channels_files.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.channels_files()

    def test_channels_get_all_user_mentions_by_channel(self):
        channels_get_all_user_mentions_by_channel = self.rocket.channels_get_all_user_mentions_by_channel(
            room_id='GENERAL').json()
        self.assertTrue(
            channels_get_all_user_mentions_by_channel.get('success'))


class TestGroups(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)
        testuser = self.rocket.users_info(username='testuser1').json()
        if not testuser.get('success'):
            testuser = self.rocket.users_create(
                'testuser1@domain.com', 'testuser1', 'password', 'testuser1').json()
            if not testuser.get('success'):
                self.fail("can't create test user")

        self.testuser_id = testuser.get('user').get('_id')
        self.test_group_name = str(uuid.uuid1())
        self.test_group_id = self.rocket.groups_create(
            self.test_group_name).json().get('group').get('_id')

    def tearDown(self):
        self.rocket.users_delete(self.testuser_id)

    def test_groups_list_all(self):
        groups_list = self.rocket.groups_list_all().json()
        self.assertTrue(groups_list.get('success'))
        self.assertIn('groups', groups_list)

    def test_groups_list(self):
        groups_list = self.rocket.groups_list().json()
        self.assertTrue(groups_list.get('success'))
        self.assertIn('groups', groups_list)

    def test_groups_info(self):
        groups_info_by_id = self.rocket.groups_info(
            room_id=self.test_group_id).json()
        self.assertTrue(groups_info_by_id.get('success'))
        self.assertIn('group', groups_info_by_id)
        self.assertEqual(groups_info_by_id.get(
            'group').get('_id'), self.test_group_id)

        groups_info_by_name = self.rocket.groups_info(
            room_name=self.test_group_name).json()
        self.assertTrue(groups_info_by_name.get('success'))
        self.assertIn('group', groups_info_by_name)
        self.assertEqual(groups_info_by_name.get(
            'group').get('_id'), self.test_group_id)

        with self.assertRaises(RocketMissingParamException):
            self.rocket.groups_info()

    def test_groups_history(self):
        groups_history = self.rocket.groups_history(
            room_id=self.test_group_id).json()
        self.assertTrue(groups_history.get('success'))
        self.assertIn('messages', groups_history)

    def test_groups_add_and_remove_moderator(self):
        me = self.rocket.me().json()
        groups_add_moderator = self.rocket.groups_add_moderator(
            self.test_group_id, me.get('_id')).json()
        self.assertTrue(groups_add_moderator.get('success'))
        groups_remove_moderator = self.rocket.groups_remove_moderator(
            self.test_group_id, me.get('_id')).json()
        self.assertTrue(groups_remove_moderator.get('success'))

    def test_groups_list_moderator(self):
        groups_list_moderator = self.rocket.groups_moderators(
            room_id=self.test_group_id).json()
        self.assertTrue(groups_list_moderator.get('success'))
        groups_list_moderator_by_name = self.rocket.groups_moderators(
            group=self.test_group_name).json()
        self.assertTrue(groups_list_moderator_by_name.get('success'))
        with self.assertRaises(RocketMissingParamException):
            self.rocket.groups_moderators()

    def test_groups_add_and_remove_owner(self):
        self.rocket.groups_invite(
            self.test_group_id, self.testuser_id)
        groups_add_owner = self.rocket.groups_add_owner(self.test_group_id,
                                                        user_id=self.testuser_id).json()
        self.assertTrue(groups_add_owner.get('success'),
                        groups_add_owner.get('error'))

        groups_remove_owner = self.rocket.groups_remove_owner(self.test_group_id,
                                                              user_id=self.testuser_id).json()
        self.assertTrue(groups_remove_owner.get('success'),
                        groups_remove_owner.get('error'))

    def test_groups_archive_unarchive(self):
        groups_archive = self.rocket.groups_archive(self.test_group_id).json()
        self.assertTrue(groups_archive.get('success'))
        groups_unarchive = self.rocket.groups_unarchive(
            self.test_group_id).json()
        self.assertTrue(groups_unarchive.get('success'))

    def test_groups_close_open(self):
        groups_close = self.rocket.groups_close(self.test_group_id).json()
        self.assertTrue(groups_close.get('success'))
        groups_open = self.rocket.groups_open(self.test_group_id).json()
        self.assertTrue(groups_open.get('success'))

    def test_groups_create_delete(self):
        name = str(uuid.uuid1())
        groups_create = self.rocket.groups_create(name).json()
        self.assertTrue(groups_create.get('success'))
        self.assertEqual(name, groups_create.get('group').get('name'))
        groups_delete = self.rocket.groups_delete(group=name).json()
        self.assertTrue(groups_delete.get('success'))
        groups_create = self.rocket.groups_create(name).json()
        self.assertTrue(groups_create.get('success'))
        room_id = groups_create.get('group').get('_id')
        groups_delete = self.rocket.groups_delete(room_id=room_id).json()
        self.assertTrue(groups_delete.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.groups_delete()

    def test_groups_get_integrations(self):
        groups_get_integrations = self.rocket.groups_get_integrations(
            room_id=self.test_group_id).json()
        self.assertTrue(groups_get_integrations.get('success'))

    def test_groups_invite(self):
        groups_invite = self.rocket.groups_invite(
            self.test_group_id, self.testuser_id).json()
        self.assertTrue(groups_invite.get('success'))

    def test_groups_kick(self):
        id_group_created = self.rocket.groups_create(
            str(uuid.uuid1())).json().get('group').get('_id')
        groups_invite = self.rocket.groups_invite(
            id_group_created, self.testuser_id).json()
        self.assertTrue(groups_invite.get('success'))
        groups_kick = self.rocket.groups_kick(
            id_group_created, self.testuser_id).json()
        self.assertTrue(groups_kick.get('success'))

    def test_groups_leave(self):
        groups_leave = self.rocket.groups_leave(self.test_group_id).json()
        self.assertFalse(groups_leave.get('success'))
        self.assertEqual(groups_leave.get('errorType'),
                         'error-you-are-last-owner')

        name = str(uuid.uuid1())
        groups_create = self.rocket.groups_create(name).json()
        self.rocket.groups_invite(room_id=groups_create.get('group').get('_id'),
                                  user_id=self.testuser_id)
        self.rocket.groups_add_owner(groups_create.get('group').get('_id'),
                                     user_id=self.testuser_id).json()
        groups_leave = self.rocket.groups_leave(
            groups_create.get('group').get('_id')).json()
        self.assertTrue(groups_leave.get('success'))

    def test_groups_rename(self):
        name = str(uuid.uuid1())
        name2 = str(uuid.uuid1())
        groups_create = self.rocket.groups_create(name).json()
        groups_rename = self.rocket.groups_rename(room_id=groups_create.get('group').get('_id'),
                                                  name=name2).json()
        self.assertTrue(groups_rename.get('success'))
        self.assertEqual(groups_rename.get('group').get('name'), name2)

    def test_groups_set_description(self):
        description = str(uuid.uuid1())
        groups_set_description = self.rocket.groups_set_description(
            self.test_group_id, description).json()
        self.assertTrue(groups_set_description.get('success'))
        self.assertEqual(groups_set_description.get('description'), description,
                         'Description does not match')

    def test_groups_set_read_only(self):
        groups_set_read_only = self.rocket.groups_set_read_only(
            self.test_group_id, True).json()
        self.assertTrue(groups_set_read_only.get('success'))
        groups_set_read_only = self.rocket.groups_set_read_only(
            self.test_group_id, False).json()
        self.assertTrue(groups_set_read_only.get('success'))

    def test_groups_set_topic(self):
        topic = str(uuid.uuid1())
        groups_set_topic = self.rocket.groups_set_topic(
            self.test_group_id, topic).json()
        self.assertTrue(groups_set_topic.get('success'))
        self.assertEqual(groups_set_topic.get('topic'), topic,
                         'Topic does not match')

    def test_groups_set_type(self):
        name = str(uuid.uuid1())
        groups_create = self.rocket.groups_create(name).json()
        self.assertTrue(groups_create.get('success'))

        groups_set_type = self.rocket.groups_set_type(
            groups_create.get('group').get('_id'), 'c').json()
        self.assertTrue(groups_set_type.get('success'))
        self.assertTrue(groups_set_type.get('group').get('t'), 'p')

        groups_set_type = self.rocket.groups_set_type(
            groups_create.get('group').get('_id'), 'p').json()
        # should fail because this is no more a group
        self.assertFalse(groups_set_type.get('success'))

    def test_groups_members(self):
        groups_members = self.rocket.groups_members(
            room_id=self.test_group_id).json()
        self.assertTrue(groups_members.get('success'))
        groups_members = self.rocket.groups_members(
            group=self.test_group_name).json()
        self.assertTrue(groups_members.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.groups_members()

    def test_groups_roles(self):
        name = str(uuid.uuid1())
        groups_create = self.rocket.groups_create(name).json()
        self.assertTrue(groups_create.get('success'))

        groups_roles = self.rocket.groups_roles(
            room_id=groups_create.get('group').get('_id')).json()
        self.assertTrue(groups_roles.get('success'))
        self.assertIsNotNone(groups_roles.get('roles'))

        groups_roles = self.rocket.groups_roles(room_name=name).json()
        self.assertTrue(groups_roles.get('success'))
        self.assertIsNotNone(groups_roles.get('roles'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.groups_roles()

    def test_groups_files(self):
        name = str(uuid.uuid1())
        groups_create = self.rocket.groups_create(name).json()
        self.assertTrue(groups_create.get('success'))

        groups_files = self.rocket.groups_files(
            room_id=groups_create.get('group').get('_id')).json()
        self.assertTrue(groups_files.get('success'))

        groups_files = self.rocket.groups_files(room_name=name).json()
        self.assertTrue(groups_files.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.groups_files()


class TestRooms(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)

    def tearDown(self):
        pass

    def test_rooms_upload(self):
        # ToDo: Find a better way to test that this endpoint actually works fine (when using json and not data fails
        # silently)
        rooms_upload = self.rocket.rooms_upload(
            'GENERAL', file='tests/avatar.png', description='hey there').json()
        self.assertTrue(rooms_upload.get('success'))

    def test_rooms_get(self):
        rooms_get = self.rocket.rooms_get().json()
        self.assertTrue(rooms_get.get('success'))

    def test_rooms_clean_history(self):
        rooms_clean_history = self.rocket.rooms_clean_history(room_id='GENERAL', latest='2016-09-30T13:42:25.304Z',
                                                              oldest='2016-05-30T13:42:25.304Z').json()
        self.assertTrue(rooms_clean_history.get('success'))

    def test_rooms_favorite(self):
        rooms_favorite = self.rocket.rooms_favorite(
            room_id='GENERAL', favorite=True).json()
        self.assertTrue(rooms_favorite.get('success'))

        rooms_favorite = self.rocket.rooms_favorite(
            room_name='general', favorite=True).json()
        self.assertTrue(rooms_favorite.get('success'))

        rooms_favorite = self.rocket.rooms_favorite(
            room_id='unexisting_channel', favorite=True).json()
        self.assertFalse(rooms_favorite.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.rooms_favorite()

    def test_rooms_info(self):
        rooms_infoby_name = self.rocket.rooms_info(room_name='general').json()
        self.assertTrue(rooms_infoby_name.get('success'))
        self.assertEqual('GENERAL', rooms_infoby_name.get('room').get('_id'))
        rooms_info_by_id = self.rocket.rooms_info(room_id='GENERAL').json()
        self.assertTrue(rooms_info_by_id.get('success'))
        self.assertEqual('GENERAL', rooms_info_by_id.get('room').get('_id'))
        with self.assertRaises(RocketMissingParamException):
            self.rocket.rooms_info()


class TestIMs(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user,
            password=self.password, username=self.user)
        # Register DM recipient
        self.recipient_user = 'user2'
        self.recipient_password = 'password'
        self.recipient_email = 'email2@domain.com'
        self.rocket.users_register(
            email=self.recipient_email, name=self.recipient_user,
            password=self.recipient_password, username=self.recipient_user)
        self.rocket = RocketChat(self.user, self.password)

    def tearDown(self):
        pass

    def test_im_create(self):
        im_create = self.rocket.im_create(self.recipient_user).json()
        self.assertTrue(im_create.get('success'))

    def test_im_send(self):
        im_create = self.rocket.im_create(self.recipient_user).json()
        room_id = im_create.get('room').get('_id')
        im_send = self.rocket.chat_post_message(room_id=room_id,
                                                text='test').json()
        self.assertTrue(im_send.get('success'))

    def test_im_list(self):
        self.rocket.im_create(self.recipient_user)
        im_list = self.rocket.im_list().json()
        self.assertTrue(im_list.get('success'))

    def test_im_close_open(self):
        im_create = self.rocket.im_create(self.recipient_user).json()
        room_id = im_create.get('room').get('_id')
        im_close = self.rocket.im_close(room_id).json()
        self.assertTrue(im_close.get('success'))
        im_open = self.rocket.im_open(room_id).json()
        self.assertTrue(im_open.get('success'))

    def test_im_set_topic(self):
        topic = 'this is my new topic'
        im_create = self.rocket.im_create(self.recipient_user).json()
        room_id = im_create.get('room').get('_id')
        im_set_topic = self.rocket.im_set_topic(room_id, topic).json()
        self.assertTrue(im_set_topic.get('success'))
        self.assertEqual(im_set_topic.get('topic'), topic,
                         'Topic set does not match topic returned')

    def test_im_list_everyone(self):
        im_list_everyone = self.rocket.im_list_everyone().json()
        self.assertTrue(im_list_everyone.get('success'))

    def test_im_history(self):
        im_create = self.rocket.im_create(self.recipient_user).json()
        room_id = im_create.get('room').get('_id')
        im_history = self.rocket.im_history(room_id).json()
        self.assertTrue(im_history.get('success'))

    def test_im_messages_others(self):
        # ToDo: Try changing the access configuration so endpoint can be successfully tested
        im_create = self.rocket.im_create(self.recipient_user).json()
        room_id = im_create.get('room').get('_id')
        im_messages_others = self.rocket.im_messages_others(room_id).json()
        self.assertFalse(im_messages_others.get('success'))

    def test_im_files(self):
        im_create = self.rocket.im_create(self.recipient_user).json()
        self.assertTrue(im_create.get('success'))

        im_files = self.rocket.im_files(
            room_id=im_create.get('room').get('_id')).json()
        self.assertTrue(im_files.get('success'))

        im_files = self.rocket.im_files(user_name=self.recipient_user).json()
        self.assertTrue(im_files.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.im_files()

    def test_im_counters(self):
        im_create = self.rocket.im_create(self.recipient_user).json()
        self.assertTrue(im_create.get('success'))

        im_counters = self.rocket.im_counters(
            room_id=im_create.get('room').get('_id')).json()
        self.assertTrue(im_counters.get('success'))

        im_counters = self.rocket.im_counters(
            user_name=self.rocket.me().json().get('_id')).json()
        self.assertTrue(im_counters.get('success'))

        with self.assertRaises(RocketMissingParamException):
            self.rocket.im_counters()


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)

    def tearDown(self):
        pass

    def test_settings(self):
        settings = self.rocket.settings().json()
        self.assertTrue(settings.get('success'))
        settings_get = self.rocket.settings_get(
            _id='API_Allow_Infinite_Count').json()
        self.assertTrue(settings_get.get('success'))
        self.assertTrue(settings_get.get('value'))
        settings_update = self.rocket.settings_update(
            _id='API_Allow_Infinite_Count', value=True).json()
        self.assertTrue(settings_update.get('success'))


class TestSubscriptions(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)

    def tearDown(self):
        pass

    def test_subscriptions_get(self):
        subscriptions_get = self.rocket.subscriptions_get().json()
        self.assertTrue(subscriptions_get.get('success'))
        self.assertIn('update', subscriptions_get)

    def test_subscriptions_get_one(self):
        subscriptions_get_one = self.rocket.subscriptions_get_one(
            room_id='GENERAL').json()
        self.assertTrue(subscriptions_get_one.get('success'))
        self.assertIn('subscription', subscriptions_get_one)

    def test_subscriptions_unread(self):
        subscriptions_unread = self.rocket.subscriptions_unread(
            room_id='GENERAL').json()
        self.assertTrue(subscriptions_unread.get('success'), 'Call did not succeed')

    def test_subscriptions_read(self):
        subscriptions_read = self.rocket.subscriptions_read(
            rid='GENERAL').json()
        self.assertTrue(subscriptions_read.get('success'), 'Call did not succeed')


class TestAssets(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)

    def tearDown(self):
        pass

    def test_assets_set_asset(self):
        assets_set_asset = self.rocket.assets_set_asset(asset_name='logo', file='tests/logo.png').json()
        self.assertTrue(assets_set_asset.get('success'))

    def test_assets_unset_asset(self):
        assets_unset_asset = self.rocket.assets_unset_asset(asset_name='logo').json()
        self.assertTrue(assets_unset_asset.get('success'))


class TestPermissions(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(
            email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)

    def tearDown(self):
        pass

    def test_permissions_list_all(self):
        permissions_list_all = self.rocket.permissions_list_all().json()
        self.assertTrue(permissions_list_all.get('success'))
        self.assertIn('update', permissions_list_all)
        self.assertIn('remove', permissions_list_all)

    def test_permissions_list_all_with_updatedSince(self):
        permissions_list_all = self.rocket.permissions_list_all(updatedSince='2017-11-25T15:08:17.248Z').json()
        self.assertTrue(permissions_list_all.get('success'))
        self.assertIn('update', permissions_list_all)
        self.assertIn('remove', permissions_list_all)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
