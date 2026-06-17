import mimetypes
import os

from rocketchat_API.APIExceptions.RocketExceptions import (
    USER_ID_OR_USERNAME_REQUIRED,
    USER_INFO_LOOKUP_REQUIRED,
    RocketMissingParamException,
)
from rocketchat_API.APISections.base import (
    RocketChatBase,
    paginated,
)

USERS_INFO = "users.info"


class RocketChatUsers(RocketChatBase):
    def me(self, **kwargs):
        """Displays information about the authenticated user."""
        return self.call_api_get("me", kwargs=kwargs)

    def users_info(
        self,
        user_id=None,
        username=None,
        import_id=None,
        email=None,
        free_switch_extension=None,
        **kwargs,
    ):
        """Gets a user's information, limited to the caller's permissions.

        Exactly one lookup parameter must be provided. ``email`` requires
        Rocket.Chat >= 8.4.0 and ``free_switch_extension`` requires >= 8.5.0.
        """
        if user_id:
            return self.call_api_get(USERS_INFO, userId=user_id, kwargs=kwargs)
        if username:
            return self.call_api_get(USERS_INFO, username=username, kwargs=kwargs)
        if import_id:
            return self.call_api_get(USERS_INFO, importId=import_id, kwargs=kwargs)
        if email:
            return self.call_api_get(USERS_INFO, email=email, kwargs=kwargs)
        if free_switch_extension:
            return self.call_api_get(
                USERS_INFO,
                freeSwitchExtension=free_switch_extension,
                kwargs=kwargs,
            )
        raise RocketMissingParamException(USER_INFO_LOOKUP_REQUIRED)

    @paginated("users")
    def users_list(self, **kwargs):
        """All of the users and their information, limited to permissions."""
        return self.call_api_get("users.list", kwargs=kwargs)

    def users_get_presence(self, user_id=None, username=None, **kwargs):
        """Gets the online presence of the a user."""
        if user_id:
            return self.call_api_get("users.getPresence", userId=user_id, kwargs=kwargs)
        if username:
            return self.call_api_get(
                "users.getPresence", username=username, kwargs=kwargs
            )
        raise RocketMissingParamException(USER_ID_OR_USERNAME_REQUIRED)

    def users_create(self, email, name, password, username, **kwargs):
        """Creates a user"""
        return self.call_api_post(
            "users.create",
            email=email,
            name=name,
            password=password,
            username=username,
            kwargs=kwargs,
        )

    def users_delete(self, user_id, **kwargs):
        """Deletes a user"""
        return self.call_api_post("users.delete", userId=user_id, **kwargs)

    def users_register(self, email, name, password, username, **kwargs):
        """Register a new user."""
        return self.call_api_post(
            "users.register",
            email=email,
            name=name,
            password=password,
            username=username,
            kwargs=kwargs,
        )

    def users_get_avatar(self, user_id=None, username=None, **kwargs):
        """Gets the URL for a user's avatar."""
        if user_id:
            return self.call_api_get("users.getAvatar", userId=user_id, kwargs=kwargs)
        if username:
            return self.call_api_get(
                "users.getAvatar", username=username, kwargs=kwargs
            )
        raise RocketMissingParamException(USER_ID_OR_USERNAME_REQUIRED)

    def users_set_avatar(self, avatar_url, **kwargs):
        """Set a user's avatar"""
        if avatar_url.startswith("http://") or avatar_url.startswith("https://"):
            return self.call_api_post(
                "users.setAvatar", avatarUrl=avatar_url, kwargs=kwargs
            )

        avatar_file = {
            "image": (
                os.path.basename(avatar_url),
                open(avatar_url, "rb"),
                mimetypes.guess_type(avatar_url)[0],
            ),
        }

        return self.call_api_post("users.setAvatar", files=avatar_file, kwargs=kwargs)

    def users_reset_avatar(self, user_id=None, username=None, **kwargs):
        """
        Reset a user's avatar to the default icon. By default, icons contain the user's initials. Permissions required, if the setting AllowUserAvatarChange is enabled:
        - edit-other-user-avatar: Permission to change other user's avatar
        - manage-moderation-actions: Permission to manage moderation actions, perform actions on reported users
        """
        if user_id:
            return self.call_api_post(
                "users.resetAvatar", userId=user_id, kwargs=kwargs
            )
        if username:
            return self.call_api_post(
                "users.resetAvatar", username=username, kwargs=kwargs
            )
        raise RocketMissingParamException(USER_ID_OR_USERNAME_REQUIRED)

    def users_create_token(self, user_id, secret, **kwargs):
        """Create a user authentication token."""
        return self.call_api_post(
            "users.createToken", userId=user_id, secret=secret, kwargs=kwargs
        )

    def users_update(self, user_id, **kwargs):
        """Update an existing user."""
        return self.call_api_post("users.update", userId=user_id, data=kwargs)

    def users_set_active_status(self, user_id, active_status, **kwargs):
        """Update user active status."""
        return self.call_api_post(
            "users.setActiveStatus",
            userId=user_id,
            activeStatus=active_status,
            kwargs=kwargs,
        )

    def users_forgot_password(self, email, **kwargs):
        """Send email to reset your password."""
        return self.call_api_post("users.forgotPassword", email=email, kwargs=kwargs)

    def users_get_preferences(self, **kwargs):
        """Gets all preferences of user."""
        return self.call_api_get("users.getPreferences", kwargs=kwargs)

    def users_set_preferences(self, user_id, data, **kwargs):
        """Set user's preferences."""
        return self.call_api_post(
            "users.setPreferences", userId=user_id, data=data, kwargs=kwargs
        )

    def users_set_status(self, message, **kwargs):
        """Sets a user Status when the status message and state is given."""
        return self.call_api_post("users.setStatus", message=message, kwargs=kwargs)
