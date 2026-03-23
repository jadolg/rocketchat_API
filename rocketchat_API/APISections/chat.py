from rocketchat_API.APIExceptions.RocketExceptions import (
    MESSAGE_RID_REQUIRED,
    RocketMissingParamException,
    ROOM_ID_OR_CHANNEL_REQUIRED,
)
from rocketchat_API.APISections.base import (
    RocketChatBase,
    paginated,
)


class RocketChatChat(RocketChatBase):
    def chat_post_message(self, text, room_id=None, channel=None, **kwargs):
        """Posts a new chat message."""
        method = "chat.postMessage"
        if room_id:
            if text:
                return self.call_api_post(
                    method, roomId=room_id, text=text, kwargs=kwargs
                )
            return self.call_api_post(method, roomId=room_id, kwargs=kwargs)
        if channel:
            if text:
                return self.call_api_post(
                    method, channel=channel, text=text, kwargs=kwargs
                )
            return self.call_api_post(method, channel=channel, kwargs=kwargs)
        raise RocketMissingParamException(ROOM_ID_OR_CHANNEL_REQUIRED)

    def chat_send_message(self, message):
        if "rid" in message:
            return self.call_api_post("chat.sendMessage", message=message)
        raise RocketMissingParamException(MESSAGE_RID_REQUIRED)

    def chat_get_message(self, msg_id, **kwargs):
        return self.call_api_get("chat.getMessage", msgId=msg_id, kwargs=kwargs)

    def chat_pin_message(self, msg_id, **kwargs):
        return self.call_api_post("chat.pinMessage", messageId=msg_id, kwargs=kwargs)

    def chat_unpin_message(self, msg_id, **kwargs):
        return self.call_api_post("chat.unPinMessage", messageId=msg_id, kwargs=kwargs)

    def chat_star_message(self, msg_id, **kwargs):
        return self.call_api_post("chat.starMessage", messageId=msg_id, kwargs=kwargs)

    def chat_unstar_message(self, msg_id, **kwargs):
        return self.call_api_post("chat.unStarMessage", messageId=msg_id, kwargs=kwargs)

    def chat_delete(self, room_id, msg_id, **kwargs):
        """Deletes a chat message."""
        return self.call_api_post(
            "chat.delete", roomId=room_id, msgId=msg_id, kwargs=kwargs
        )

    def chat_update(self, room_id, msg_id, text, **kwargs):
        """Updates the text of the chat message."""
        return self.call_api_post(
            "chat.update", roomId=room_id, msgId=msg_id, text=text, kwargs=kwargs
        )

    def chat_react(self, msg_id, emoji="smile", **kwargs):
        """Updates the text of the chat message."""
        return self.call_api_post(
            "chat.react", messageId=msg_id, emoji=emoji, kwargs=kwargs
        )

    @paginated("messages")
    def chat_search(self, room_id, search_text, **kwargs):
        """Search for messages in a channel by id and text message."""
        return self.call_api_get(
            "chat.search", roomId=room_id, searchText=search_text, kwargs=kwargs
        )

    @paginated("receipts")
    def chat_get_message_read_receipts(self, message_id, **kwargs):
        """Get Message Read Receipts"""
        return self.call_api_get(
            "chat.getMessageReadReceipts", messageId=message_id, kwargs=kwargs
        )

    @paginated("messages")
    def chat_get_starred_messages(self, room_id, **kwargs):
        """Retrieve starred messages."""
        return self.call_api_get(
            "chat.getStarredMessages", roomId=room_id, kwargs=kwargs
        )

    def chat_report_message(self, message_id, description, **kwargs):
        """Reports a message."""
        return self.call_api_post(
            "chat.reportMessage",
            messageId=message_id,
            description=description,
            kwargs=kwargs,
        )

    def chat_follow_message(self, mid, **kwargs):
        """Follows a chat message to the message's channel."""
        return self.call_api_post("chat.followMessage", mid=mid, kwargs=kwargs)

    @paginated("messages")
    def chat_get_thread_messages(self, thread_msg_id, **kwargs):
        """Get thread messages."""
        return self.call_api_get(
            "chat.getThreadMessages",
            tmid=thread_msg_id,
            kwargs=kwargs,
        )

    @paginated("messages")
    def chat_get_mentioned_messages(self, room_id, **kwargs):
        """Get the messages in which you are mentioned (users are mentioned with the @ symbol)."""
        return self.call_api_get(
            "chat.getMentionedMessages",
            roomId=room_id,
            kwargs=kwargs,
        )

    def chat_unfollow_message(self, mid, **kwargs):
        """Unfollow a message."""
        return self.call_api_post("chat.unfollowMessage", mid=mid, kwargs=kwargs)

    @paginated("messages")
    def chat_get_deleted_messages(self, room_id, since, **kwargs):
        """Get deleted messages from a specific date."""
        return self.call_api_get(
            "chat.getDeletedMessages", roomId=room_id, since=since, kwargs=kwargs
        )

    @paginated("messages")
    def chat_get_pinned_messages(self, room_id, **kwargs):
        """Get pinned messages of a room."""
        return self.call_api_get(
            "chat.getPinnedMessages", roomId=room_id, kwargs=kwargs
        )

    def chat_ignore_user(self, rid, user_id, ignore=True, **kwargs):
        """Ignore or unignore a user in chat."""
        return self.call_api_get(
            "chat.ignoreUser", rid=rid, userId=user_id, ignore=ignore, kwargs=kwargs
        )

    def chat_sync_thread_list(self, rid, updated_since, **kwargs):
        """List threads in a room updated since a given ISO date."""
        return self.call_api_get(
            "chat.syncThreadsList", rid=rid, updatedSince=updated_since, kwargs=kwargs
        )

    def chat_sync_thread_messages(self, tmid, updated_since, **kwargs):
        """List the messages in a thread along with any data updates from a specified date."""
        return self.call_api_get(
            "chat.syncThreadMessages",
            tmid=tmid,
            updatedSince=updated_since,
            kwargs=kwargs,
        )

    def chat_sync_messages(self, room_id, last_update, **kwargs):
        """List the messages in a room along with any data updates from a specified date."""
        return self.call_api_get(
            "chat.syncMessages", roomId=room_id, lastUpdate=last_update, kwargs=kwargs
        )

    @paginated("threads")
    def chat_get_threads_list(self, rid, **kwargs):
        """Get a list of the thread conversations in a room."""
        return self.call_api_get("chat.getThreadsList", rid=rid, kwargs=kwargs)

    def chat_get_url_preview(self, room_id, url, **kwargs):
        """Use this endpoint to get a URL preview that can be used in the send and update message endpoints."""
        return self.call_api_get(
            "chat.getURLPreview", roomId=room_id, url=url, kwargs=kwargs
        )

    @paginated("messages")
    def chat_get_discussions(self, room_id, **kwargs):
        """Get the discussions in a room."""
        return self.call_api_get("chat.getDiscussions", roomId=room_id, kwargs=kwargs)
