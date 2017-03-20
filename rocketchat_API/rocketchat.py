import requests

from rocketchat_API.APIExceptions.RocketExceptions import RocketConnectionException, RocketAuthenticationException


class RocketChat:
    headers = {}
    ssl_verify = True
    API_path = '/api/v1/'

    def __init__(self, user, password, server_url='http://127.0.0.1:3000', ssl_verify=True):
        """Creates a RocketChat object and does login on the specified server"""
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
        return requests.get(self.server_url + self.API_path + method + '?' +
                            '&'.join([i + '=' + str(args[i]) for i in args.keys()]),
                            headers=self.headers,
                            verify=self.ssl_verify)

    def __call_api_post(self, method, **kwargs):
        args = self.__reduce_kwargs(kwargs)
        return requests.post(self.server_url + self.API_path + method,
                             data=args,
                             headers=self.headers,
                             verify=self.ssl_verify)

    # Authentication

    def me(self, **kwargs):
        """	Displays information about the authenticated user."""
        return self.__call_api_get('me', kwargs=kwargs)

    def logout(self, **kwargs):
        """Invalidate your REST rocketchat_API authentication token."""
        return self.__call_api_get('logout', kwargs=kwargs)

    # Miscellaneous information

    def info(self, **kwargs):
        """Information about the Rocket.Chat server."""
        return self.__call_api_get('info', kwargs=kwargs)

    # Users

    def users_info(self, user_id, **kwargs):
        """Gets a user’s information, limited to the caller’s permissions."""
        return self.__call_api_get('users.info', userId=user_id, kwargs=kwargs)

    def users_list(self, **kwargs):
        """All of the users and their information, limited to permissions."""
        return self.__call_api_get('users.list', kwargs=kwargs)

    def users_get_presence(self, user_id, **kwargs):
        """Gets the online presence of the a user."""
        return self.__call_api_get('users.getPresence', userId=user_id, kwargs=kwargs)

    # Chat

    def chat_post_message(self, room_id, text, **kwargs):
        """Posts a new chat message."""
        return self.__call_api_post('chat.postMessage', roomId=room_id, text=text, kwargs=kwargs)

    def chat_delete(self, room_id, msg_id, **kwargs):
        """Deletes a chat message."""
        return self.__call_api_post('chat.delete', roomId=room_id, msgId=msg_id, kwargs=kwargs)

    def chat_update(self, room_id, msg_id, text, **kwargs):
        """Updates the text of the chat message."""
        return self.__call_api_post('chat.update', roomId=room_id, msgId=msg_id, text=text, kwargs=kwargs)

    # Channels

    def channels_list(self, **kwargs):
        """Retrieves all of the channels from the server."""
        return self.__call_api_get('channels.list', kwargs=kwargs)

    def channels_list_joined(self, **kwargs):
        """Lists all of the channels the calling user has joined"""
        return self.__call_api_get('channels.list.joined', kwargs=kwargs)

    def channels_info(self, room_id, **kwargs):
        """Gets a channel’s information."""
        return self.__call_api_get('channels.info', roomId=room_id, kwargs=kwargs)

    def channels_history(self, room_id, **kwargs):
        """Retrieves the messages from a channel."""
        return self.__call_api_get('channels.history', roomId=room_id, kwargs=kwargs)

    # Groups

    def groups_list(self, **kwargs):
        """List the private groups the caller is part of."""
        return self.__call_api_get('groups.list', kwargs=kwargs)

    def groups_history(self, room_id, **kwargs):
        """Retrieves the messages from a private group."""
        return self.__call_api_get('groups.history', roomId=room_id, kwargs=kwargs)

    # IM
    def im_list(self, **kwargs):
        """List the private im chats for logged user"""
        return self.__call_api_get('im.list', kwargs=kwargs)

    def im_history(self, room_id, **kwargs):
        """Retrieves the history for a private im chat"""
        return self.__call_api_get('im.history', roomId=room_id, kwargs=kwargs)

    # Statistics

    def statistics(self, **kwargs):
        """Retrieves the current statistics"""
        return self.__call_api_get('statistics', kwargs=kwargs)
