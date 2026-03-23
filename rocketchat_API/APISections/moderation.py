from rocketchat_API.APISections.base import RocketChatBase, paginated


class RocketChatModeration(RocketChatBase):
    @paginated("reports")
    def moderation_reports_by_users(self, **kwargs):
        """Retrieves all the reported messages grouped by users. Permission required: view-moderation-console"""
        return self.call_api_get("moderation.reportsByUsers", kwargs=kwargs)

    @paginated("reports")
    def moderation_user_reports(self, **kwargs):
        """Get the list of reported users. Permission required: view-moderation-console"""
        return self.call_api_get("moderation.userReports", kwargs=kwargs)

    def moderation_user_reported_messages(self, user_id, **kwargs):
        """Retrieve all reported messages of a user. Permission required: view-moderation-console"""
        return self.call_api_get(
            "moderation.user.reportedMessages", userId=user_id, kwargs=kwargs
        )

    def moderation_user_reports_by_user_id(self, user_id, **kwargs):
        """Get the details of a specific user's reports. Permission required: view-moderation-console"""
        return self.call_api_get(
            "moderation.user.reportsByUserId", userId=user_id, kwargs=kwargs
        )

    @paginated("reports")
    def moderation_reports(self, msg_id, **kwargs):
        """Retrieve all the reports of a single message. A message can have many reports. Permission required: view-moderation-console"""
        return self.call_api_get("moderation.reports", msgId=msg_id, kwargs=kwargs)

    def moderation_report_info(self, report_id, **kwargs):
        """Get more details of a single report. Permission required: view-moderation-console"""
        return self.call_api_get(
            "moderation.reportInfo", reportId=report_id, kwargs=kwargs
        )

    def moderation_report_user(self, user_id, description, **kwargs):
        """Report a user."""
        return self.call_api_post(
            "moderation.reportUser",
            userId=user_id,
            description=description,
            kwargs=kwargs,
        )

    def moderation_dismiss_reports(self, user_id=None, msg_id=None, **kwargs):
        """You can dismiss all the reports of a particular user by the userId. You can also dismiss the report of a message by the msgId. Permission required: manage-moderation-actions"""
        if user_id:
            return self.call_api_post(
                "moderation.dismissReports", userId=user_id, kwargs=kwargs
            )
        return self.call_api_post(
            "moderation.dismissReports", msgId=msg_id, kwargs=kwargs
        )

    def moderation_dismiss_user_reports(self, user_id, **kwargs):
        """Dismiss a specific reported user from the list of reported users. Permission required: manage-moderation-actions"""
        return self.call_api_post(
            "moderation.dismissUserReports", userId=user_id, kwargs=kwargs
        )

    def moderation_user_delete_reported_messages(self, user_id, **kwargs):
        """Delete all the reports of messages that belongs to user. Permission required: manage-moderation-actions"""
        return self.call_api_post(
            "moderation.user.deleteReportedMessages", userId=user_id, kwargs=kwargs
        )
