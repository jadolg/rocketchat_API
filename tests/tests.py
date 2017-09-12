import unittest

from rocketchat_API.APIExceptions.RocketExceptions import RocketAuthenticationException, RocketMissingParamException
from rocketchat_API.rocketchat import RocketChat


class TestServer(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()

    def test_info(self):
        info = self.rocket.info().json()

        self.assertTrue('info' in info)
        self.assertTrue(info.get('success'))


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.rocket = RocketChat()
        self.user = 'user1'
        self.password = 'password'
        self.email = 'email@domain.com'
        self.rocket.users_register(email=self.email, name=self.user, password=self.password, username=self.user)

    def test_login(self):
        login = self.rocket.login(self.user, self.password).json()

        with self.assertRaises(RocketAuthenticationException):
            self.rocket.login(self.user, 'bad_password')

        self.assertEqual(login.get('status'), 'success')
        self.assertTrue('authToken' in login.get('data'))
        self.assertTrue('userId' in login.get('data'))

    def test_me(self):
        self.rocket.login(self.user, self.password).json()
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
        users_info = self.rocket.users_info(user_id=login.get('data').get('userId')).json()
        self.assertTrue(users_info.get('success'))
        self.assertEqual(users_info.get('user').get('name'), self.user)

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
        login = self.rocket.login(self.user, self.password).json()

        self.rocket.login(self.user, self.password).json()
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

    def test_users_set_avatar(self):
        login = self.rocket.login(self.user, self.password).json()
        users_set_avatar = self.rocket.users_set_avatar(avatar_url='tests/avatar.png').json()
        self.assertTrue(users_set_avatar.get('success'), users_set_avatar.get('error'))

        # ToDo: Users.setAvatar calls https://secure.gravatar.com/avatar/ before actually do anything
        users_set_avatar = self.rocket.users_set_avatar(avatar_url='http://182.17.0.1:9999/avatar.png').json()
        self.assertTrue(users_set_avatar.get('success'), users_set_avatar.get('error'))


if __name__ == '__main__':
    unittest.main(warnings='ignore')
