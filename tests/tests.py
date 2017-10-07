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
        self.rocket.users_register(email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)

    def test_info(self):
        info = self.rocket.info().json()

        self.assertTrue('info' in info)
        self.assertTrue(info.get('success'))

    def test_statistics(self):
        statistics = self.rocket.statistics().json()
        self.assertTrue(statistics.get('success'))


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)

    def test_login(self):
        login = self.rocket.login(self.user, self.password).json()

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

    def test_users_get_presence(self):
        login = self.rocket.login(self.user, self.password).json()
        users_get_presence = self.rocket.users_get_presence(user_id=login.get('data').get('userId')).json()
        self.assertTrue(users_get_presence.get('success'))

        users_get_presence_by_name = self.rocket.users_get_presence(username=self.user).json()
        self.assertTrue(users_get_presence_by_name.get('success'))

    def test_users_get_avatar(self):
        login = self.rocket.login(self.user, self.password).json()

        users_get_avatar = self.rocket.users_get_avatar(user_id='no_user')
        self.assertEqual(users_get_avatar.status_code, 400)

        users_get_avatar = self.rocket.users_get_avatar(user_id=login.get('data').get('userId'))
        self.assertGreater(len(users_get_avatar.text), 0)

        users_get_avatar = self.rocket.users_get_avatar(username=self.user)
        self.assertGreater(len(users_get_avatar.text), 0)

        with self.assertRaises(RocketMissingParamException):
            self.rocket.users_get_avatar()

    def test_users_reset_avatar(self):
        login = self.rocket.login(self.user, self.password).json()
        users_reset_avatar = self.rocket.users_reset_avatar(user_id=login.get('data').get('userId')).json()
        self.assertTrue(users_reset_avatar.get('success'))

        users_reset_avatar = self.rocket.users_reset_avatar(username=self.user).json()
        self.assertTrue(users_reset_avatar.get('success'))

    def test_users_create_token(self):
        login = self.rocket.login(self.user, self.password).json()
        users_create_token = self.rocket.users_create_token(user_id=login.get('data').get('userId')).json()
        self.assertTrue(users_create_token.get('success'))
        self.assertIn('authToken', users_create_token.get('data'))
        self.assertIn('userId', users_create_token.get('data'))

    def test_users_create_update_delete(self):
        users_create = self.rocket.users_create(email='email2@domain.com', name='user2', password=self.password,
                                                username='user2').json()
        self.assertTrue(users_create.get('success'), users_create.get('error'))

        users_update = self.rocket.users_update(users_create.get('user').get('_id'), 'anewemail@domain.com',
                                                name='newname', password=self.password, username='newusername').json()
        self.assertTrue(users_update.get('success'))
        self.assertEqual(users_update.get('user').get('email'), 'anewemail@domain.com')
        self.assertEqual(users_update.get('user').get('name'), 'newname')
        self.assertEqual(users_update.get('user').get('username'), 'newusername')

        users_delete = self.rocket.users_delete(users_create.get('user').get('_id')).json()
        self.assertTrue(users_delete.get('success'))

    def test_users_set_avatar_from_file(self):
        users_set_avatar = self.rocket.users_set_avatar(avatar_url='tests/avatar.png').json()
        self.assertTrue(users_set_avatar.get('success'), users_set_avatar.get('error'))

    def test_users_set_avatar_from_url(self):
        # ToDo: Users.setAvatar calls https://secure.gravatar.com/avatar/ before actually do anything
        users_set_avatar = self.rocket.users_set_avatar(avatar_url='http://182.17.0.1:9999/avatar.png').json()
        self.assertTrue(users_set_avatar.get('success'), users_set_avatar.get('error'))


class TestChat(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket = RocketChat(self.user, self.password)

    def test_chat_post_update_delete_message(self):
        chat_post_message = self.rocket.chat_post_message("hello", channel='GENERAL').json()
        self.assertEqual(chat_post_message.get('channel'), 'GENERAL')
        self.assertEqual(chat_post_message.get('message').get('msg'), 'hello')
        self.assertTrue(chat_post_message.get('success'))

        chat_update = self.rocket.chat_update(room_id=chat_post_message.get('channel'),
                                              msg_id=chat_post_message.get('message').get('_id'),
                                              text='hello again').json()

        self.assertEqual(chat_update.get('message').get('msg'), 'hello again')
        self.assertTrue(chat_update.get('success'))

        chat_delete = self.rocket.chat_delete(room_id=chat_post_message.get('channel'),
                                              msg_id=chat_post_message.get('message').get('_id')).json()
        self.assertTrue(chat_delete.get('success'))


class TestChannels(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(email=self.email, name=self.user, password=self.password, username=self.user)
        self.rocket.channels_add_owner('GENERAL', username=self.user)
        self.rocket = RocketChat(self.user, self.password)
        self.testuser = self.rocket.users_create('email0@domain.com', 'user0', 'password', 'user0').json()

    def tearDown(self):
        self.rocket.users_delete(self.testuser.get('user').get('_id'))

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

    def test_channels_history(self):
        channels_history = self.rocket.channels_history(room_id='GENERAL').json()
        self.assertTrue(channels_history.get('success'))
        self.assertIn('messages', channels_history)

    def test_channels_add_all(self):
        channels_add_all = self.rocket.channels_add_all('GENERAL').json()
        self.assertTrue(channels_add_all.get('success'))

    def test_channels_add_and_remove_moderator(self):
        me = self.rocket.me().json()
        channels_add_moderator = self.rocket.channels_add_moderator('GENERAL', me.get('_id')).json()
        self.assertTrue(channels_add_moderator.get('success'))
        channels_remove_moderator = self.rocket.channels_remove_moderator('GENERAL', me.get('_id')).json()
        self.assertTrue(channels_remove_moderator.get('success'))

    def test_channels_add_and_remove_owner(self):
        channels_add_owner = self.rocket.channels_add_owner('GENERAL',
                                                            user_id=self.testuser.get('user').get('_id')).json()
        self.assertTrue(channels_add_owner.get('success'), channels_add_owner.get('error'))
        channels_remove_owner = self.rocket.channels_remove_owner('GENERAL',
                                                                  user_id=self.testuser.get('user').get('_id')).json()
        self.assertTrue(channels_remove_owner.get('success'), channels_remove_owner.get('error'))

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

    def test_channels_create(self):
        name = str(uuid.uuid1())
        channels_create = self.rocket.channels_create(name).json()
        self.assertTrue(channels_create.get('success'))
        self.assertEqual(name, channels_create.get('channel').get('name'))

    def test_channels_get_integrations(self):
        channels_get_integrations = self.rocket.channels_get_integrations(room_id='GENERAL').json()
        self.assertTrue(channels_get_integrations.get('success'))

    def test_channels_invite(self):
        channels_invite = self.rocket.channels_invite('GENERAL', self.testuser.get('user').get('_id')).json()
        self.assertTrue(channels_invite.get('success'))
        self.assertIn(self.testuser.get('user').get('username'), channels_invite.get('channel').get('usernames'))

    def test_channels_kick(self):
        channels_kick = self.rocket.channels_kick('GENERAL', self.testuser.get('user').get('_id')).json()
        self.assertTrue(channels_kick.get('success'))
        self.assertNotIn(self.testuser.get('user').get('username'), channels_kick.get('channel').get('usernames'))

    def test_channels_leave(self):
        channels_leave = self.rocket.channels_leave('GENERAL').json()
        self.assertFalse(channels_leave.get('success'))
        self.assertEqual(channels_leave.get('errorType'), 'error-you-are-last-owner')

        name = str(uuid.uuid1())
        channels_create = self.rocket.channels_create(name).json()
        self.rocket.channels_invite(room_id=channels_create.get('channel').get('_id'),
                                    user_id=self.testuser.get('user').get('_id'))
        self.rocket.channels_add_owner(channels_create.get('channel').get('_id'),
                                       user_id=self.testuser.get('user').get('_id')).json()
        channels_leave = self.rocket.channels_leave(channels_create.get('channel').get('_id')).json()
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
        channels_set_description = self.rocket.channels_set_description('GENERAL', description).json()
        self.assertTrue(channels_set_description.get('success'))
        self.assertEqual(channels_set_description.get('description'), description,
                         'Description does not match')

    def test_channels_set_join_code(self):
        join_code = str(uuid.uuid1())
        channels_set_join_code = self.rocket.channels_set_join_code('GENERAL', join_code).json()
        self.assertTrue(channels_set_join_code.get('success'))

    def test_channels_set_read_only(self):
        channels_set_read_only = self.rocket.channels_set_read_only('GENERAL', True).json()
        self.assertTrue(channels_set_read_only.get('success'))
        channels_set_read_only = self.rocket.channels_set_read_only('GENERAL', False).json()
        self.assertTrue(channels_set_read_only.get('success'))

    def test_channels_set_topic(self):
        topic = str(uuid.uuid1())
        channels_set_topic = self.rocket.channels_set_topic('GENERAL', topic).json()
        self.assertTrue(channels_set_topic.get('success'))
        self.assertEqual(channels_set_topic.get('topic'), topic,
                         'Topic does not match')

    def test_channels_set_type(self):
        name = str(uuid.uuid1())
        channels_create = self.rocket.channels_create(name).json()
        self.assertTrue(channels_create.get('success'))

        channels_set_type = self.rocket.channels_set_type(channels_create.get('channel').get('_id'), 'p').json()
        self.assertTrue(channels_set_type.get('success'))
        self.assertTrue(channels_set_type.get('channel').get('t'), 'p')

        channels_set_type = self.rocket.channels_set_type(channels_create.get('channel').get('_id'), 'c').json()
        self.assertFalse(channels_set_type.get('success'))  # should fail because this is no more a channel


if __name__ == '__main__':
    unittest.main(warnings='ignore')
