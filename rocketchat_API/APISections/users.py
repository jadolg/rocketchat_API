import hashlib
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

USERS_GET_STATUS = "users.getStatus"

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
        if avatar_url.startswith(("http://", "https://")):
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

    @paginated("users")
    def users_list_by_status(self, **kwargs):
        """Lists users filtered by status, role or search term.

        Accepts ``status`` (active or deactivated), ``hasLoggedIn``, ``type``,
        ``roles``, ``searchTerm`` and ``inactiveReason``. Requires ``view-d-room``,
        and ``view-outside-room`` when Apply_permission_view-outside-room is on.
        """
        return self.call_api_get("users.listByStatus", kwargs=kwargs)

    def users_get_username_suggestion(self, **kwargs):
        """Gets a free username suggestion for the authenticated user."""
        return self.call_api_get("users.getUsernameSuggestion", kwargs=kwargs)

    def users_get_avatar_suggestion(self, **kwargs):
        """Gets avatar suggestions from the user's connected OAuth services."""
        return self.call_api_get("users.getAvatarSuggestion", kwargs=kwargs)

    def users_check_username_availability(self, username, **kwargs):
        """Checks whether a username is available."""
        return self.call_api_get(
            "users.checkUsernameAvailability", username=username, kwargs=kwargs
        )

    def users_presence(self, **kwargs):
        """Gets the presence of users.

        Accepts ``ids`` and ``from`` (ISO 8601 datetime). Without ``from``, the
        presence of all users is returned.
        """
        return self.call_api_get("users.presence", kwargs=kwargs)

    def users_autocomplete(self, selector, **kwargs):
        """Autocompletes users. ``selector`` is a JSON string, e.g. ``{"term": "ab"}``."""
        return self.call_api_get("users.autocomplete", selector=selector, kwargs=kwargs)

    def users_get_status(self, user_id=None, username=None, **kwargs):
        """Gets the status of a user by ``user_id`` or ``username``.

        Returns the authenticated user's status if neither is given.
        """
        if user_id:
            return self.call_api_get(USERS_GET_STATUS, userId=user_id, kwargs=kwargs)
        if username:
            return self.call_api_get(USERS_GET_STATUS, username=username, kwargs=kwargs)
        return self.call_api_get(USERS_GET_STATUS, kwargs=kwargs)

    def users_list_teams(self, user_id, **kwargs):
        """Lists the teams a user belongs to. Seeing all of them needs view-all-teams."""
        return self.call_api_get("users.listTeams", userId=user_id, kwargs=kwargs)

    def users_generate_personal_access_token(self, token_name, **kwargs):
        """Generates a personal access token. Accepts ``bypassTwoFactor``.

        Requires ``create-personal-access-tokens`` and 2FA.
        """
        return self.call_api_post(
            "users.generatePersonalAccessToken", tokenName=token_name, kwargs=kwargs
        )

    def users_regenerate_personal_access_token(self, token_name, **kwargs):
        """Regenerates an existing personal access token.

        Requires ``create-personal-access-tokens`` and 2FA.
        """
        return self.call_api_post(
            "users.regeneratePersonalAccessToken", tokenName=token_name, kwargs=kwargs
        )

    def users_get_personal_access_tokens(self, **kwargs):
        """Lists the personal access tokens of the authenticated user.

        Requires ``create-personal-access-tokens``.
        """
        return self.call_api_get("users.getPersonalAccessTokens", kwargs=kwargs)

    def users_remove_personal_access_token(self, token_name, **kwargs):
        """Removes a personal access token.

        Requires ``create-personal-access-tokens`` and 2FA.
        """
        return self.call_api_post(
            "users.removePersonalAccessToken", tokenName=token_name, kwargs=kwargs
        )

    def users_request_data_download(self, full_export=False, **kwargs):
        """Requests an export of the authenticated user's data.

        The User Data Download feature must be configured in the workspace.
        """
        return self.call_api_get(
            "users.requestDataDownload",
            fullExport=str(full_export).lower(),
            kwargs=kwargs,
        )

    def users_deactivate_idle(self, days_idle, **kwargs):
        """Deactivates users idle for ``days_idle`` days. Accepts ``role``.

        Requires ``edit-other-user-active-status``.
        """
        return self.call_api_post(
            "users.deactivateIdle", daysIdle=days_idle, kwargs=kwargs
        )

    def users_send_confirmation_email(self, email, **kwargs):
        """Sends the email verification again. Rate limited to one per 60 seconds."""
        return self.call_api_post(
            "users.sendConfirmationEmail", email=email, kwargs=kwargs
        )

    def users_update_own_basic_info(self, data, **kwargs):
        """Updates the authenticated user's own profile. Accepts ``customFields``."""
        return self.call_api_post("users.updateOwnBasicInfo", data=data, kwargs=kwargs)

    def users_2fa_send_email_code(self, email_or_username, **kwargs):
        """Sends an email 2FA code to the user."""
        return self.call_api_post(
            "users.2fa.sendEmailCode", emailOrUsername=email_or_username, kwargs=kwargs
        )

    def users_2fa_enable_email(self, **kwargs):
        """Enables email 2FA. The user must have a verified email."""
        return self.call_api_post("users.2fa.enableEmail", kwargs=kwargs)

    def users_2fa_disable_email(self, **kwargs):
        """Disables email 2FA. Requires a 2FA code."""
        return self.call_api_post("users.2fa.disableEmail", kwargs=kwargs)

    def users_enable_totp(self, **kwargs):
        """Starts TOTP setup, returns the ``secret`` and a ``url`` for the QR code.

        Finish it with ``users_validate_totp``. Requires 2FA.
        """
        return self.call_api_post("users.enableTotp", kwargs=kwargs)

    def users_validate_totp(self, code, **kwargs):
        """Finishes TOTP setup with a code from the app, returns the backup codes."""
        return self.call_api_post("users.validateTotp", code=code, kwargs=kwargs)

    def users_disable_totp(self, code, **kwargs):
        """Disables TOTP."""
        return self.call_api_post("users.disableTotp", code=code, kwargs=kwargs)

    def users_regenerate_totp_codes(self, code, **kwargs):
        """Regenerates the TOTP backup codes. The previous ones stop working."""
        return self.call_api_post("users.regenerateTotpCodes", code=code, kwargs=kwargs)

    def users_totp_codes_remaining(self, **kwargs):
        """Gets how many TOTP backup codes are left."""
        return self.call_api_get("users.totpCodesRemaining", kwargs=kwargs)

    def users_reset_totp(self, **kwargs):
        """Resets TOTP of a user (``userId`` or ``username``), or your own if omitted.

        Resetting another user's needs ``edit-other-user-totp``.
        """
        return self.call_api_post("users.resetTOTP", kwargs=kwargs)

    def users_reset_e2e_key(self, **kwargs):
        """Resets E2E key of a user (``userId`` or ``username``), or your own if omitted.

        Resetting another user's needs ``edit-other-user-e2ee``.
        """
        return self.call_api_post("users.resetE2EKey", kwargs=kwargs)

    def users_logout(self, **kwargs):
        """Logs out the given user (``userId``), or yourself if omitted.

        Logging out another user needs ``logout-other-user``.
        """
        return self.call_api_post("users.logout", kwargs=kwargs)

    def users_logout_other_clients(self, **kwargs):
        """Logs out all other sessions of the authenticated user."""
        return self.call_api_post("users.logoutOtherClients", kwargs=kwargs)

    def users_remove_other_tokens(self, **kwargs):
        """Removes all login tokens except the current one."""
        return self.call_api_post("users.removeOtherTokens", kwargs=kwargs)

    def users_delete_own_account(self, password, **kwargs):
        """Deletes the authenticated user's account.

        Requires the Accounts_AllowDeleteOwnAccount setting. Accepts
        ``confirmRelinquish`` to delete it even if it is the last owner of a room.
        """
        return self.call_api_post(
            "users.deleteOwnAccount",
            body={
                # Rocket.Chat expects the password as a SHA-256 hex digest
                "password": hashlib.sha256(password.encode()).hexdigest(),
                **kwargs,
            },
        )
