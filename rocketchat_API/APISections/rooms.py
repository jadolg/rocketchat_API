import mimetypes
import os

from rocketchat_API.APIExceptions.RocketExceptions import RocketMissingParamException
from rocketchat_API.APISections.base import RocketChatBase


class RocketChatRooms(RocketChatBase):
    def rooms_upload(self, rid, file, **kwargs):
        """Post a message with attached file to a dedicated room."""
        files = {
            "file": (
                os.path.basename(file),
                open(file, "rb"),
                mimetypes.guess_type(file)[0],
            ),
        }
        return self.call_api_post(
            "rooms.upload/" + rid, kwargs=kwargs, use_json=False, files=files
        )

    def rooms_get(self, **kwargs):
        """Get all opened rooms for this user."""
        return self.call_api_get("rooms.get", kwargs=kwargs)

    def rooms_clean_history(self, room_id, latest, oldest, **kwargs):
        """Cleans up a room, removing messages from the provided time range."""
        return self.call_api_post(
            "rooms.cleanHistory",
            roomId=room_id,
            latest=latest,
            oldest=oldest,
            kwargs=kwargs,
        )

    def rooms_favorite(self, room_id=None, room_name=None, favorite=True):
        """Favorite or unfavorite room."""
        if room_id is not None:
            return self.call_api_post(
                "rooms.favorite", roomId=room_id, favorite=favorite
            )
        if room_name is not None:
            return self.call_api_post(
                "rooms.favorite", roomName=room_name, favorite=favorite
            )
        raise RocketMissingParamException("roomId or roomName required")

    def rooms_info(self, room_id=None, room_name=None):
        """Retrieves the information about the room."""
        if room_id is not None:
            return self.call_api_get("rooms.info", roomId=room_id)
        if room_name is not None:
            return self.call_api_get("rooms.info", roomName=room_name)
        raise RocketMissingParamException("roomId or roomName required")

    def rooms_admin_rooms(self, **kwargs):
        """ Retrieves all rooms (requires the view-room-administration permission)."""
        return self.call_api_get("rooms.adminRooms", kwargs=kwargs)

    def rooms_create_discussion(self, prid, t_name, **kwargs):
        """Creates a new discussion for room. It requires at least one of the following permissions:
        start-discussion OR start-discussion-other-user, AND must be with the following setting enabled:
        Discussion_enabled."""
        return self.call_api_post(
            "rooms.createDiscussion", prid=prid, t_name=t_name, kwargs=kwargs
        )
