from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from rocketchat_API.APISections.base import RocketChatBase


class RocketChatChat(RocketChatBase):
    def chat_post_message(self, text, room_id=None, channel=None, **kwargs):
        """Posts a new chat message."""
        if room_id:
            if text:
                return self.call_api_post(
                    "chat.postMessage", roomId=room_id, text=text, kwargs=kwargs
                )
            return self.call_api_post("chat.postMessage", roomId=room_id, kwargs=kwargs)
        if channel:
            if text:
                return self.call_api_post(
                    "chat.postMessage", channel=channel, text=text, kwargs=kwargs
                )
            return self.call_api_post(
                "chat.postMessage", channel=channel, kwargs=kwargs
            )
        raise RocketMissingParamException("roomId or channel required")

    def chat_send_message(self, message):
        if "rid" in message:
            return self.call_api_post("chat.sendMessage", message=message)
        raise RocketMissingParamException("message.rid required")

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

    def chat_search(self, room_id, search_text, **kwargs):
        """Search for messages in a channel by id and text message."""
        return self.call_api_get(
            "chat.search", roomId=room_id, searchText=search_text, kwargs=kwargs
        )

    def chat_get_message_read_receipts(self, message_id, **kwargs):
        """Get Message Read Receipts"""
        return self.call_api_get(
            "chat.getMessageReadReceipts", messageId=message_id, kwargs=kwargs
        )

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
