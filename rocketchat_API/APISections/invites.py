from rocketchat_API.APISections.base import RocketChatBase


class RocketChatInvites(RocketChatBase):
    def find_or_create_invite(self, rid, days, max_uses):
        """
        Creates or return an existing invite with the specified parameters.
        Requires the create-invite-links permission
        """
        return self.call_api_post(
            "findOrCreateInvite", rid=rid, days=days, maxUses=max_uses
        )

    def list_invites(self, **kwargs):
        """Lists all of the invites on the server. Requires the create-invite-links permission."""
        return self.call_api_get("listInvites", kwargs=kwargs)

    def remove_invite(self, invite_id, **kwargs):
        """Deletes an invite. Requires the create-invite-links permission."""
        return self.call_api_delete("removeInvite/{}".format(invite_id))

    def use_invite_token(self, token, **kwargs):
        """Reports to the server that an invite token was used."""
        return self.call_api_post("useInviteToken", token=token, kwargs=kwargs)

    def validate_invite_token(self, token, **kwargs):
        """Checks if an invite token is valid."""
        return self.call_api_post("validateInviteToken", token=token, kwargs=kwargs)

    def send_invitation_email(self, emails, **kwargs):
        """Sends invitation emails to a list of email addresses."""
        return self.call_api_post("sendInvitationEmail", emails=emails, kwargs=kwargs)
