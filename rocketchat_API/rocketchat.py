# -*-coding:utf-8-*-

import json

import requests

from rocketchat_API.APIExceptions.RocketExceptions import RocketConnectionException, RocketAuthenticationException


class RocketChat:
    headers = {}
    API_path = '/api/v1/'

    def __init__(self, user, password, server_url='http://127.0.0.1:3000', ssl_verify=True, proxies=None):
        """Creates a RocketChat object and does login on the specified server"""
        self.server_url = server_url
        self.proxies = proxies
        self.ssl_verify = ssl_verify
        login = requests.post(server_url + self.API_path + 'login',
                              data={'username': user, 'password': password},
                              verify=ssl_verify,
                              proxies=self.proxies)
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
                            verify=self.ssl_verify,
                            proxies=self.proxies)

    def __call_api_post(self, method, **kwargs):
        args = json.dumps(self.__reduce_kwargs(kwargs))
        return requests.post(self.server_url + self.API_path + method,
                             data=args,
                             headers=self.headers,
                             verify=self.ssl_verify,
                             proxies=self.proxies)

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

    def users_create(self, email, name, password, username, **kwargs):
        """Creates a user"""
        return self.__call_api_post('users.create', email=email, name=name, password=password, username=username,
                                    kwargs=kwargs)

    def users_delete(self, user_id, **kwargs):
        """Deletes a user"""
        return self.__call_api_post('users.delete', userId=user_id, **kwargs)

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

    def channels_add_all(self, room_id, **kwargs):
        """Adds all of the users of the Rocket.Chat server to the channel."""
        return self.__call_api_post('channels.addAll', roomId=room_id, kwargs=kwargs)

    def channels_add_moderator(self, room_id, user_id, **kwargs):
        """Gives the role of moderator for a user in the current channel."""
        return self.__call_api_post('channels.addModerator', roomId=room_id, userId=user_id, kwargs=kwargs)

    def channels_remove_moderator(self, room_id, user_id, **kwargs):
        """Removes the role of moderator from a user in the current channel."""
        return self.__call_api_post('channels.removeModerator', roomId=room_id, userId=user_id, kwargs=kwargs)

    def channels_add_owner(self, room_id, user_id, **kwargs):
        """Gives the role of owner for a user in the current channel."""
        return self.__call_api_post('channels.addOwner', roomId=room_id, userId=user_id, kwargs=kwargs)

    def channels_remove_owner(self, room_id, user_id, **kwargs):
        """Removes the role of owner from a user in the current channel."""
        return self.__call_api_post('channels.removeOwner', roomId=room_id, userId=user_id, kwargs=kwargs)

    def channels_archive(self, room_id, **kwargs):
        """Archives a channel."""
        return self.__call_api_post('channels.archive', roomId=room_id, kwargs=kwargs)

    def channels_unarchive(self, room_id, **kwargs):
        """Unarchives a channel."""
        return self.__call_api_post('channels.unarchive', roomId=room_id, kwargs=kwargs)

    # this endpoint isn't working properly
    def channels_clean_history(self, room_id, latest, oldest, **kwargs):
        """Cleans up a channel, removing messages from the provided time range."""
        return self.__call_api_post('channels.cleanHistory', roomId=room_id, latest=latest, oldest=oldest,
                                    kwargs=kwargs)

    def channels_close(self, room_id, **kwargs):
        """Removes the channel from the user’s list of channels."""
        return self.__call_api_post('channels.close', roomId=room_id, kwargs=kwargs)

    def channels_open(self, room_id, **kwargs):
        """Adds the channel back to the user’s list of channels."""
        return self.__call_api_post('channels.open', roomId=room_id, kwargs=kwargs)

    def channels_create(self, name, **kwargs):
        """Creates a new public channel, optionally including users."""
        return self.__call_api_post('channels.create', name=name, kwargs=kwargs)

    def channels_get_integrations(self, room_id, **kwargs):
        """Retrieves the integrations which the channel has"""
        return self.__call_api_get('channels.getIntegrations', roomId=room_id, kwargs=kwargs)

    def channels_invite(self, room_id, user_id, **kwargs):
        """Adds a user to the channel."""
        return self.__call_api_post('channels.invite', roomId=room_id, userId=user_id, kwargs=kwargs)

    def channels_kick(self, room_id, user_id, **kwargs):
        """Removes a user from the channel."""
        return self.__call_api_post('channels.kick', roomId=room_id, userId=user_id, kwargs=kwargs)

    def channels_leave(self, room_id, **kwargs):
        """Causes the callee to be removed from the channel."""
        return self.__call_api_post('channels.leave', roomId=room_id, kwargs=kwargs)

    def channels_rename(self, room_id, name, **kwargs):
        """Changes the name of the channel."""
        return self.__call_api_post('channels.rename', roomId=room_id, name=name, kwargs=kwargs)

    def channels_set_description(self, room_id, description, **kwargs):
        """Sets the description for the channel."""
        return self.__call_api_post('channels.setDescription', roomId=room_id, description=description, kwargs=kwargs)

    def channels_set_join_code(self, room_id, join_code, **kwargs):
        """Sets the code required to join the channel."""
        return self.__call_api_post('channels.setJoinCode', roomId=room_id, joinCode=join_code, kwargs=kwargs)

    def channels_set_read_only(self, room_id, read_only, **kwargs):
        """Sets whether the channel is read only or not."""
        return self.__call_api_post('channels.setReadOnly', roomId=room_id, readOnly=bool(read_only), kwargs=kwargs)

    def channels_set_topic(self, room_id, topic, **kwargs):
        """Sets the topic for the channel."""
        return self.__call_api_post('channels.setTopic', roomId=room_id, topic=topic, kwargs=kwargs)

    def channels_set_type(self, room_id, a_type, **kwargs):
        """Sets the type of room this channel should be. The type of room this channel should be, either c or p."""
        return self.__call_api_post('channels.setType', roomId=room_id, type=a_type, kwargs=kwargs)

    # Groups

    def groups_list(self, **kwargs):
        """List the private groups the caller is part of."""
        return self.__call_api_get('groups.list', kwargs=kwargs)

    def groups_history(self, room_id, **kwargs):
        """Retrieves the messages from a private group."""
        return self.__call_api_get('groups.history', roomId=room_id, kwargs=kwargs)

    def groups_add_moderator(self, room_id, user_id, **kwargs):
        """Gives the role of moderator for a user in the current groups."""
        return self.__call_api_post('groups.addModerator', roomId=room_id, userId=user_id, kwargs=kwargs)

    def groups_remove_moderator(self, room_id, user_id, **kwargs):
        """Removes the role of moderator from a user in the current groups."""
        return self.__call_api_post('groups.removeModerator', roomId=room_id, userId=user_id, kwargs=kwargs)

    def groups_add_owner(self, room_id, user_id, **kwargs):
        """Gives the role of owner for a user in the current Group."""
        return self.__call_api_post('groups.addOwner', roomId=room_id, userId=user_id, kwargs=kwargs)

    def groups_remove_owner(self, room_id, user_id, **kwargs):
        """Removes the role of owner from a user in the current Group."""
        return self.__call_api_post('groups.removeOwner', roomId=room_id, userId=user_id, kwargs=kwargs)

    def groups_archive(self, room_id, **kwargs):
        """Archives a private group, only if you’re part of the group."""
        return self.__call_api_post('groups.archive', roomId=room_id, kwargs=kwargs)

    def groups_unarchive(self, room_id, **kwargs):
        """Unarchives a private group."""
        return self.__call_api_post('groups.unarchive', roomId=room_id, kwargs=kwargs)

    def groups_close(self, room_id, **kwargs):
        """Removes the private group from the user’s list of groups, only if you’re part of the group."""
        return self.__call_api_post('groups.close', roomId=room_id, kwargs=kwargs)

    def groups_create(self, name, **kwargs):
        """Creates a new private group, optionally including users, only if you’re part of the group."""
        return self.__call_api_post('groups.create', name=name, kwargs=kwargs)

    def groups_get_integrations(self, room_id, **kwargs):
        """Retrieves the integrations which the group has"""
        return self.__call_api_get('groups.getIntegrations', roomId=room_id, kwargs=kwargs)

    def groups_info(self, room_id, **kwargs):
        """GRetrieves the information about the private group, only if you’re part of the group."""
        return self.__call_api_get('groups.info', roomId=room_id, kwargs=kwargs)

    def groups_invite(self, room_id, user_id, **kwargs):
        """Adds a user to the private group."""
        return self.__call_api_post('groups.invite', roomId=room_id, userId=user_id, kwargs=kwargs)

    def groups_kick(self, room_id, user_id, **kwargs):
        """Removes a user from the private group."""
        return self.__call_api_post('groups.kick', roomId=room_id, userId=user_id, kwargs=kwargs)

    def groups_leave(self, room_id, **kwargs):
        """Causes the callee to be removed from the private group, if they’re part of it and are not the last owner."""
        return self.__call_api_post('groups.leave', roomId=room_id, kwargs=kwargs)

    def groups_open(self, room_id, **kwargs):
        """Adds the private group back to the user’s list of private groups."""
        return self.__call_api_post('groups.open', roomId=room_id, kwargs=kwargs)

    def groups_rename(self, room_id, name, **kwargs):
        """Changes the name of the private group."""
        return self.__call_api_post('groups.rename', roomId=room_id, name=name, kwargs=kwargs)

    def groups_set_description(self, room_id, description, **kwargs):
        """Sets the description for the private group."""
        return self.__call_api_post('groups.setDescription', roomId=room_id, description=description, kwargs=kwargs)

    def groups_set_read_only(self, room_id, read_only, **kwargs):
        """Sets whether the group is read only or not."""
        return self.__call_api_post('groups.setReadOnly', roomId=room_id, readOnly=bool(read_only), kwargs=kwargs)

    def groups_set_topic(self, room_id, topic, **kwargs):
        """Sets the topic for the private group."""
        return self.__call_api_post('groups.setTopic', roomId=room_id, topic=topic, kwargs=kwargs)

    def groups_set_type(self, room_id, a_type, **kwargs):
        """Sets the type of room this group should be. The type of room this channel should be, either c or p."""
        return self.__call_api_post('groups.setType', roomId=room_id, type=a_type, kwargs=kwargs)

    # IM
    def im_list(self, **kwargs):
        """List the private im chats for logged user"""
        return self.__call_api_get('im.list', kwargs=kwargs)

    def im_list_everyone(self, **kwargs):
        """List all direct message the caller in the server."""
        return self.__call_api_get('im.list.everyone', kwargs=kwargs)

    def im_history(self, room_id, **kwargs):
        """Retrieves the history for a private im chat"""
        return self.__call_api_get('im.history', roomId=room_id, kwargs=kwargs)

    def im_open(self, room_id, **kwargs):
        """Adds the direct message back to the user’s list of direct messages."""
        return self.__call_api_post('im.open', roomId=room_id, kwargs=kwargs)

    def im_close(self, room_id, **kwargs):
        """Removes the direct message from the user’s list of direct messages."""
        return self.__call_api_post('im.close', roomId=room_id, kwargs=kwargs)

    def im_messages_others(self, room_id, **kwargs):
        """Retrieves the messages from any direct message in the server"""
        return self.__call_api_get('im.messages.others', roomId=room_id, kwargs=kwargs)

    def im_set_topic(self, room_id, topic, **kwargs):
        """Sets the topic for the direct message"""
        return self.__call_api_post('im.setTopic', roomId=room_id, topic=topic, kwargs=kwargs)

    # Statistics

    def statistics(self, **kwargs):
        """Retrieves the current statistics"""
        return self.__call_api_get('statistics', kwargs=kwargs)

    # Settings

    def settings_get(self, _id):
        """Gets the setting for the provided _id."""
        return self.__call_api_get('settings/' + _id)

    def settings_update(self, _id, value):
        """Updates the setting for the provided _id."""
        return self.__call_api_post('settings/' + _id, value=value)
