# -*-coding:utf-8-*-
import logging
import mimetypes
import os

import requests

from rocketchat_API.APIExceptions.RocketExceptions import RocketConnectionException, RocketAuthenticationException, \
    RocketMissingParamException

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class RocketChat:
    API_path = '/api/v1/'

    def __init__(self, user=None, password=None, auth_token=None, user_id=None,
                 server_url='http://127.0.0.1:3000', ssl_verify=True, proxies=None,
                 timeout=30):
        """Creates a RocketChat object and does login on the specified server"""
        self.headers = {}
        self.server_url = server_url
        self.proxies = proxies
        self.ssl_verify = ssl_verify
        self.timeout = timeout
        if user and password:
            self.login(user, password)
        if auth_token and user_id:
            self.headers['X-Auth-Token'] = auth_token
            self.headers['X-User-Id'] = user_id

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
                            '&'.join([i + '=' + str(args[i])
                                      for i in args.keys()]),
                            headers=self.headers,
                            verify=self.ssl_verify,
                            proxies=self.proxies,
                            timeout=self.timeout
                            )

    def __call_api_post(self, method, files=None, use_json=True, **kwargs):
        reduced_args = self.__reduce_kwargs(kwargs)
        # Since pass is a reserved word in Python it has to be injected on the request dict
        # Some methods use pass (users.register) and others password (users.create)
        if 'password' in reduced_args and method != 'users.create':
            reduced_args['pass'] = reduced_args['password']
        if use_json:
            return requests.post(self.server_url + self.API_path + method,
                                 json=reduced_args,
                                 files=files,
                                 headers=self.headers,
                                 verify=self.ssl_verify,
                                 proxies=self.proxies,
                                 timeout=self.timeout
                                 )
        else:
            return requests.post(self.server_url + self.API_path + method,
                                 data=reduced_args,
                                 files=files,
                                 headers=self.headers,
                                 verify=self.ssl_verify,
                                 proxies=self.proxies,
                                 timeout=self.timeout
                                 )

    # Authentication

    def login(self, user, password):
        login_request = requests.post(self.server_url + self.API_path + 'login',
                                      data={'username': user,
                                            'password': password},
                                      verify=self.ssl_verify,
                                      proxies=self.proxies)
        if login_request.status_code == 401:
            raise RocketAuthenticationException()

        if login_request.status_code == 200:
            if login_request.json().get('status') == "success":
                self.headers['X-Auth-Token'] = login_request.json().get('data').get('authToken')
                self.headers['X-User-Id'] = login_request.json().get('data').get('userId')
                return login_request
            else:
                raise RocketAuthenticationException()
        else:
            raise RocketConnectionException()

    def me(self, **kwargs):
        """	Displays information about the authenticated user."""
        return self.__call_api_get('me', kwargs=kwargs)

    def logout(self, **kwargs):
        """Invalidate your REST rocketchat_API authentication token."""
        return self.__call_api_post('logout', kwargs=kwargs)

    # Miscellaneous information

    def info(self, **kwargs):
        """Information about the Rocket.Chat server."""
        return self.__call_api_get('info', kwargs=kwargs)

    def directory(self, query, **kwargs):
        """Search by users or channels on all server."""
        if isinstance(query, dict):
            query = str(query).replace("'", '"')

        return self.__call_api_get('directory', query=query, kwargs=kwargs)

    def spotlight(self, query, **kwargs):
        """Searches for users or rooms that are visible to the user."""
        return self.__call_api_get('spotlight', query=query, kwargs=kwargs)

    def users_get_preferences(self, **kwargs):
        """Gets all preferences of user."""
        return self.__call_api_get('users.getPreferences', kwargs=kwargs)

    def users_set_preferences(self, user_id, data, **kwargs):
        """Set user’s preferences."""
        return self.__call_api_post('users.setPreferences', userId=user_id, data=data, kwargs=kwargs)

    # Users

    def users_info(self, user_id=None, username=None, **kwargs):
        """Gets a user’s information, limited to the caller’s permissions."""
        if user_id:
            return self.__call_api_get('users.info', userId=user_id, kwargs=kwargs)
        elif username:
            return self.__call_api_get('users.info', username=username, kwargs=kwargs)
        else:
            raise RocketMissingParamException('userID or username required')

    def users_list(self, **kwargs):
        """All of the users and their information, limited to permissions."""
        return self.__call_api_get('users.list', kwargs=kwargs)

    def users_get_presence(self, user_id=None, username=None, **kwargs):
        """Gets the online presence of the a user."""
        if user_id:
            return self.__call_api_get('users.getPresence', userId=user_id, kwargs=kwargs)
        elif username:
            return self.__call_api_get('users.getPresence', username=username, kwargs=kwargs)
        else:
            raise RocketMissingParamException('userID or username required')

    def users_create(self, email, name, password, username, **kwargs):
        """Creates a user"""
        return self.__call_api_post('users.create', email=email, name=name, password=password, username=username,
                                    kwargs=kwargs)

    def users_delete(self, user_id, **kwargs):
        """Deletes a user"""
        return self.__call_api_post('users.delete', userId=user_id, **kwargs)

    def users_register(self, email, name, password, username, **kwargs):
        """Register a new user."""
        return self.__call_api_post('users.register', email=email, name=name, password=password, username=username,
                                    kwargs=kwargs)

    def users_get_avatar(self, user_id=None, username=None, **kwargs):
        """Gets the URL for a user’s avatar."""
        if user_id:
            return self.__call_api_get('users.getAvatar', userId=user_id, kwargs=kwargs)
        elif username:
            return self.__call_api_get('users.getAvatar', username=username, kwargs=kwargs)
        else:
            raise RocketMissingParamException('userID or username required')

    def users_set_avatar(self, avatar_url, **kwargs):
        """Set a user’s avatar"""
        if avatar_url.startswith('http://') or avatar_url.startswith('https://'):
            return self.__call_api_post('users.setAvatar', avatarUrl=avatar_url, kwargs=kwargs)
        else:
            avatar_file = {"image": open(avatar_url, "rb")}
            return self.__call_api_post('users.setAvatar', files=avatar_file, kwargs=kwargs)

    def users_reset_avatar(self, user_id=None, username=None, **kwargs):
        """Reset a user’s avatar"""
        if user_id:
            return self.__call_api_post('users.resetAvatar', userId=user_id, kwargs=kwargs)
        elif username:
            return self.__call_api_post('users.resetAvatar', username=username, kwargs=kwargs)
        else:
            raise RocketMissingParamException('userID or username required')

    def users_create_token(self, user_id=None, username=None, **kwargs):
        """Create a user authentication token."""
        if user_id:
            return self.__call_api_post('users.createToken', userId=user_id, kwargs=kwargs)
        elif username:
            return self.__call_api_post('users.createToken', username=username, kwargs=kwargs)
        else:
            raise RocketMissingParamException('userID or username required')

    def users_update(self, user_id, **kwargs):
        """Update an existing user."""
        return self.__call_api_post('users.update', userId=user_id, data=kwargs)

    def users_forgot_password(self, email, **kwargs):
        """Send email to reset your password."""
        return self.__call_api_post('users.forgotPassword', email=email, data=kwargs)

    # Chat

    def chat_post_message(self, text, room_id=None, channel=None, **kwargs):
        """Posts a new chat message."""
        if room_id:
            return self.__call_api_post('chat.postMessage', roomId=room_id, text=text, kwargs=kwargs)
        elif channel:
            return self.__call_api_post('chat.postMessage', channel=channel, text=text, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or channel required')

    def chat_get_message(self, msg_id, **kwargs):
        return self.__call_api_get('chat.getMessage', msgId=msg_id, kwargs=kwargs)

    def chat_pin_message(self, msg_id, **kwargs):
        return self.__call_api_post('chat.pinMessage', messageId=msg_id, kwargs=kwargs)

    def chat_unpin_message(self, msg_id, **kwargs):
        return self.__call_api_post('chat.unPinMessage', messageId=msg_id, kwargs=kwargs)

    def chat_star_message(self, msg_id, **kwargs):
        return self.__call_api_post('chat.starMessage', messageId=msg_id, kwargs=kwargs)

    def chat_unstar_message(self, msg_id, **kwargs):
        return self.__call_api_post('chat.unStarMessage', messageId=msg_id, kwargs=kwargs)

    def chat_delete(self, room_id, msg_id, **kwargs):
        """Deletes a chat message."""
        return self.__call_api_post('chat.delete', roomId=room_id, msgId=msg_id, kwargs=kwargs)

    def chat_update(self, room_id, msg_id, text, **kwargs):
        """Updates the text of the chat message."""
        return self.__call_api_post('chat.update', roomId=room_id, msgId=msg_id, text=text, kwargs=kwargs)

    def chat_react(self, msg_id, emoji='smile', **kwargs):
        """Updates the text of the chat message."""
        return self.__call_api_post('chat.react', messageId=msg_id, emoji=emoji, kwargs=kwargs)

    def chat_search(self, room_id, search_text, **kwargs):
        """Search for messages in a channel by id and text message."""
        return self.__call_api_get('chat.search', roomId=room_id, searchText=search_text, kwargs=kwargs)

    def chat_get_message_read_receipts(self, message_id, **kwargs):
        """Get Message Read Receipts"""
        return self.__call_api_get('chat.getMessageReadReceipts', messageId=message_id, kwargs=kwargs)

    # Channels

    def channels_list(self, **kwargs):
        """Retrieves all of the channels from the server."""
        return self.__call_api_get('channels.list', kwargs=kwargs)

    def channels_list_joined(self, **kwargs):
        """Lists all of the channels the calling user has joined"""
        return self.__call_api_get('channels.list.joined', kwargs=kwargs)

    def channels_info(self, room_id=None, channel=None, **kwargs):
        """Gets a channel’s information."""
        if room_id:
            return self.__call_api_get('channels.info', roomId=room_id, kwargs=kwargs)
        elif channel:
            return self.__call_api_get('channels.info', roomName=channel, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or channel required')

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

    def channels_moderators(self, room_id=None, channel=None, **kwargs):
        """Lists all moderators of a channel."""
        if room_id:
            return self.__call_api_get('channels.moderators', roomId=room_id, kwargs=kwargs)
        elif channel:
            return self.__call_api_get('channels.moderators', roomName=channel, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or channel required')

    def channels_add_owner(self, room_id, user_id=None, username=None, **kwargs):
        """Gives the role of owner for a user in the current channel."""
        if user_id:
            return self.__call_api_post('channels.addOwner', roomId=room_id, userId=user_id, kwargs=kwargs)
        elif username:
            return self.__call_api_post('channels.addOwner', roomId=room_id, username=username, kwargs=kwargs)
        else:
            raise RocketMissingParamException('userID or username required')

    def channels_remove_owner(self, room_id, user_id, **kwargs):
        """Removes the role of owner from a user in the current channel."""
        return self.__call_api_post('channels.removeOwner', roomId=room_id, userId=user_id, kwargs=kwargs)

    def channels_archive(self, room_id, **kwargs):
        """Archives a channel."""
        return self.__call_api_post('channels.archive', roomId=room_id, kwargs=kwargs)

    def channels_unarchive(self, room_id, **kwargs):
        """Unarchives a channel."""
        return self.__call_api_post('channels.unarchive', roomId=room_id, kwargs=kwargs)

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

    def channels_set_announcement(self, room_id, announce, **kwargs):
        """Sets the announcement for the channel."""
        return self.__call_api_post('channels.setAnnouncement', roomId=room_id, announcement=announce, kwargs=kwargs)

    def channels_set_custom_fields(self, rid, custom_fields):
        """Sets the custom fields for the channel."""
        return self.__call_api_post('channels.setCustomFields', roomId=rid, customFields=custom_fields)

    def channels_delete(self, room_id=None, channel=None, **kwargs):
        """Delete a public channel."""
        if room_id:
            return self.__call_api_post('channels.delete', roomId=room_id, kwargs=kwargs)
        elif channel:
            return self.__call_api_post('channels.delete', roomName=channel, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or channel required')

    def channels_members(self, room_id=None, channel=None, **kwargs):
        """Lists all channel users."""
        if room_id:
            return self.__call_api_get('channels.members', roomId=room_id, kwargs=kwargs)
        elif channel:
            return self.__call_api_get('channels.members', roomName=channel, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or channel required')

    def channels_roles(self, room_id=None, room_name=None, **kwargs):
        """Lists all user’s roles in the channel."""
        if room_id:
            return self.__call_api_get('channels.roles', roomId=room_id, kwargs=kwargs)
        elif room_name:
            return self.__call_api_get('channels.roles', roomName=room_name, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or room_name required')

    def channels_files(self, room_id=None, room_name=None, **kwargs):
        """Retrieves the files from a channel."""
        if room_id:
            return self.__call_api_get('channels.files', roomId=room_id, kwargs=kwargs)
        elif room_name:
            return self.__call_api_get('channels.files', roomName=room_name, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or room_name required')

    def channels_get_all_user_mentions_by_channel(self, room_id, **kwargs):
        """Gets all the mentions of a channel."""
        return self.__call_api_get('channels.getAllUserMentionsByChannel', roomId=room_id, kwargs=kwargs)

    # Groups

    def groups_list_all(self, **kwargs):
        """
        List all the private groups on the server.
        The calling user must have the 'view-room-administration' right
        """
        return self.__call_api_get('groups.listAll', kwargs=kwargs)

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

    def groups_moderators(self, room_id=None, group=None, **kwargs):
        """Lists all moderators of a group."""
        if room_id:
            return self.__call_api_get('groups.moderators', roomId=room_id, kwargs=kwargs)
        elif group:
            return self.__call_api_get('groups.moderators', roomName=group, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or group required')

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

    def groups_info(self, room_id=None, room_name=None, **kwargs):
        """GRetrieves the information about the private group, only if you’re part of the group."""
        if room_id:
            return self.__call_api_get('groups.info', roomId=room_id, kwargs=kwargs)
        elif room_name:
            return self.__call_api_get('groups.info', roomName=room_name, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or roomName required')

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

    def groups_delete(self, room_id=None, group=None, **kwargs):
        """Delete a private group."""
        if room_id:
            return self.__call_api_post('groups.delete', roomId=room_id, kwargs=kwargs)
        elif group:
            return self.__call_api_post('groups.delete', roomName=group, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or group required')

    def groups_members(self, room_id=None, group=None, **kwargs):
        """Lists all group users."""
        if room_id:
            return self.__call_api_get('groups.members', roomId=room_id, kwargs=kwargs)
        elif group:
            return self.__call_api_get('groups.members', roomName=group, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or group required')

    def groups_roles(self, room_id=None, room_name=None, **kwargs):
        """Lists all user’s roles in the private group."""
        if room_id:
            return self.__call_api_get('groups.roles', roomId=room_id, kwargs=kwargs)
        elif room_name:
            return self.__call_api_get('groups.roles', roomName=room_name, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or room_name required')

    def groups_files(self, room_id=None, room_name=None, **kwargs):
        """Retrieves the files from a private group."""
        if room_id:
            return self.__call_api_get('groups.files', roomId=room_id, kwargs=kwargs)
        elif room_name:
            return self.__call_api_get('groups.files', roomName=room_name, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or room_name required')

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

    def im_create(self, username, **kwargs):
        """Create a direct message session with another user."""
        return self.__call_api_post('im.create', username=username, kwargs=kwargs)

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

    def im_files(self, room_id=None, user_name=None, **kwargs):
        """Retrieves the files from a direct message."""
        if room_id:
            return self.__call_api_get('im.files', roomId=room_id, kwargs=kwargs)
        elif user_name:
            return self.__call_api_get('im.files', username=user_name, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or username required')

    def im_counters(self, room_id=None, user_name=None, **kwargs):
        """Gets counters of direct messages."""
        if room_id:
            return self.__call_api_get('im.counters', roomId=room_id, kwargs=kwargs)
        elif user_name:
            return self.__call_api_get('im.counters', username=user_name, kwargs=kwargs)
        else:
            raise RocketMissingParamException('roomId or username required')

    # Statistics

    def statistics(self, **kwargs):
        """Retrieves the current statistics"""
        return self.__call_api_get('statistics', kwargs=kwargs)

    def statistics_list(self, **kwargs):
        """Selectable statistics about the Rocket.Chat server."""
        return self.__call_api_get('statistics.list', kwargs=kwargs)

    # Settings

    def settings_get(self, _id):
        """Gets the setting for the provided _id."""
        return self.__call_api_get('settings/' + _id)

    def settings_update(self, _id, value):
        """Updates the setting for the provided _id."""
        return self.__call_api_post('settings/' + _id, value=value)

    def settings(self):
        """List all private settings."""
        return self.__call_api_get('settings')

    # Rooms

    def rooms_upload(self, rid, file, **kwargs):
        """Post a message with attached file to a dedicated room."""
        files = {
            'file': (os.path.basename(file), open(file, 'rb'), mimetypes.guess_type(file)[0]),
        }
        return self.__call_api_post('rooms.upload/' + rid, kwargs=kwargs, use_json=False, files=files)

    def rooms_get(self, **kwargs):
        """Get all opened rooms for this user."""
        return self.__call_api_get('rooms.get', kwargs=kwargs)

    def rooms_clean_history(self, room_id, latest, oldest, **kwargs):
        """Cleans up a room, removing messages from the provided time range."""
        return self.__call_api_post('rooms.cleanHistory', roomId=room_id, latest=latest, oldest=oldest, kwargs=kwargs)

    def rooms_favorite(self, room_id=None, room_name=None, favorite=True):
        """Favorite or unfavorite room."""
        if room_id is not None:
            return self.__call_api_post('rooms.favorite', roomId=room_id, favorite=favorite)
        elif room_name is not None:
            return self.__call_api_post('rooms.favorite', roomName=room_name, favorite=favorite)
        else:
            raise RocketMissingParamException('roomId or roomName required')

    def rooms_info(self, room_id=None, room_name=None):
        """Retrieves the information about the room."""
        if room_id is not None:
            return self.__call_api_get('rooms.info', roomId=room_id)
        elif room_name is not None:
            return self.__call_api_get('rooms.info', roomName=room_name)
        else:
            raise RocketMissingParamException('roomId or roomName required')

    # Subscriptions

    def subscriptions_get(self, **kwargs):
        """Get all subscriptions."""
        return self.__call_api_get('subscriptions.get', kwargs=kwargs)

    def subscriptions_get_one(self, room_id, **kwargs):
        """Get the subscription by room id."""
        return self.__call_api_get('subscriptions.getOne', roomId=room_id, kwargs=kwargs)

    def subscriptions_unread(self, room_id, **kwargs):
        """Mark messages as unread by roomId or from a message"""
        return self.__call_api_post('subscriptions.unread', roomId=room_id, kwargs=kwargs)

    def subscriptions_read(self, rid, **kwargs):
        """Mark room as read"""
        return self.__call_api_post('subscriptions.read', rid=rid, kwargs=kwargs)

    # Assets

    def assets_set_asset(self, asset_name, file, **kwargs):
        """Set an asset image by name."""
        content_type = mimetypes.MimeTypes().guess_type(file)
        files = {
            asset_name: (file, open(file, 'rb'), content_type[0], {'Expires': '0'}),
        }
        return self.__call_api_post('assets.setAsset', kwargs=kwargs, use_json=False, files=files)

    def assets_unset_asset(self, asset_name):
        """Unset an asset by name"""
        return self.__call_api_post('assets.unsetAsset', assetName=asset_name)

    # Permissions
    def permissions_list_all(self, **kwargs):
        """Returns all permissions from the server."""
        return self.__call_api_get('permissions.listAll', kwargs=kwargs)
