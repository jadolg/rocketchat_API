from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from rocketchat_API.APISections.base import RocketChatBase


class RocketChatChat(RocketChatBase):
    def chat_post_message(self, text, room_id=None, channel=None, **kwargs):
        """Posts a new chat message."""
        if not (channel or room_id):
            raise RocketMissingParamException("roomId or channel required")

        text = "" if text is None else text

        payload = {"text": text, **kwargs}
        if channel:
            payload["channel"] = channel
        if room_id:
            payload["roomId"] = room_id

        self._sanitize_payload_text_fields(payload)

        return self.call_api_post("chat.postMessage", kwargs=payload)

    @staticmethod
    def _sanitize_text(value: str) -> str:
        """Return value with common double-escaped control sequences normalized."""
        if not isinstance(value, str):
            return value
        return (
            value.replace("\\n", "\n")
            .replace("\\r", "\r")
            .replace("\\t", "\t")
            .replace("\\b", "\b")
            .replace("\\f", "\f")
        )

    @staticmethod
    def _sanitize_payload_text_fields(payload: dict) -> dict:
        """
        In-place sanitize of typical text fields in chat payloads:
        - payload["text"]
        - payload["attachments"][i]["text"]

        Returns the mutated payload for convenience.
        """
        if not isinstance(payload, dict):
            return payload

        if "text" in payload and isinstance(payload["text"], str):
            payload["text"] = RocketChatChat._sanitize_text(payload["text"])

        attachments = payload.get("attachments")
        if isinstance(attachments, list):
            for att in attachments:
                if isinstance(att, dict) and isinstance(att.get("text"), str):
                    att["text"] = RocketChatChat._sanitize_text(att["text"])

        return payload

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

    def chat_get_thread_messages(self, thread_msg_id, **kwargs):
        """Get thread messages."""
        return self.call_api_get(
            "chat.getThreadMessages",
            tmid=thread_msg_id,
            kwargs=kwargs,
        )

    def chat_get_mentioned_messages(self, room_id, **kwargs):
        """Get the messages in which you are mentioned (users are mentioned with the @ symbol)."""
        return self.call_api_get(
            "chat.getMentionedMessages",
            roomId=room_id,
            kwargs=kwargs,
        )
