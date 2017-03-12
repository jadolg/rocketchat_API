from pprint import pprint

import requests

from API.APIExceptions.RocketExceptions import RocketConnectionException, RocketAuthenticationException


class RocketChat:
    headers = {}
    ssl_verify = True
    API_path = '/api/v1/'

    def __init__(self, user, password, server_url='http://127.0.0.1:3000', ssl_verify=True):
        self.server_url = server_url
        login = requests.post(server_url + self.API_path + 'login',
                              data={'username': user, 'password': password},
                              verify=ssl_verify)
        if login.status_code == 401:
            raise RocketAuthenticationException()

        if login.status_code == 200:
            if login.json().get('status') == "success":
                self.headers['X-Auth-Token'] = login.json().get('data').get('authToken')
                self.headers['X-User-Id'] = login.json().get('data').get('userId')
            else:
                raise RocketAuthenticationException()
        else:
            raise RocketConnectionException()

    @staticmethod
    def __reduce_kwargs(kwargs):
        if 'kwargs' in kwargs:
            for arg in kwargs['kwargs'].keys():
                kwargs[arg] = kwargs['kwargs'][arg]

            del kwargs['kwargs']
        return kwargs

    def __call_api_get(self, method, **kwargs):
        args = self.__reduce_kwargs(kwargs)
        r = requests.get(self.server_url + self.API_path + method + '?' +
                         '&'.join([i + '=' + str(args[i]) for i in args.keys()]),
                         headers=self.headers,
                         verify=self.ssl_verify)
        pprint(r.url)
        return r

    def __call_api_post(self, method, **kwargs):
        args = self.__reduce_kwargs(kwargs)
        return requests.post(self.server_url + self.API_path + method,
                             data=args,
                             headers=self.headers,
                             verify=self.ssl_verify)

    # Authentication

    def me(self):
        return self.__call_api_get('me')

    # Miscellaneous information

    def info(self):
        return self.__call_api_get('info')

    # Users

    def users_info(self, user_id, **kwargs):
        return self.__call_api_get('users.info', userId=user_id, kwargs=kwargs)

    def users_list(self, **kwargs):
        return self.__call_api_get('users.list', kwargs=kwargs)

    def users_get_presence(self, user_id):
        return self.__call_api_get('users.getPresence', userId=user_id)

    # Chat

    def chat_post_message(self, room_id, text, **kwargs):
        return self.__call_api_post('chat.postMessage', roomId=room_id, text=text, kwargs=kwargs)

    def chat_delete(self, room_id, msg_id, **kwargs):
        return self.__call_api_post('chat.delete', roomId=room_id, msgId=msg_id, kwargs=kwargs)

    def chat_update(self, room_id, msg_id, text, **kwargs):
        return self.__call_api_post('chat.update', roomId=room_id, msgId=msg_id, text=text, kwargs=kwargs)

    # Channels

    def channels_list(self, **kwargs):
        return self.__call_api_get('channels.list', kwargs=kwargs)

    def channels_info(self, room_id, **kwargs):
        return self.__call_api_get('channels.info', roomId=room_id, kwargs=kwargs)

    def channels_history(self, room_id, **kwargs):
        return self.__call_api_get('channels.history', roomId=room_id, kwargs=kwargs)

    # Groups

    def groups_list(self, **kwargs):
        return self.__call_api_get('groups.list', kwargs=kwargs)

    def groups_history(self, room_id, **kwargs):
        return self.__call_api_get('groups.history', roomId=room_id, kwargs=kwargs)

    # IM
    def im_list(self, **kwargs):
        return self.__call_api_get('im.list', kwargs=kwargs)

    def im_history(self, room_id, **kwargs):
        return self.__call_api_get('im.history', roomId=room_id, kwargs=kwargs)
