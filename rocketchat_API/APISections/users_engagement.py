from rocketchat_API.APISections.base import RocketChatBase


class RocketChatUsersEngagement(RocketChatBase):
    def engagement_dashboard_new_users(self, start, end, **kwargs):
        """
        Retrieve the metrics of newly registered users during a specific period.
        Permission required: view-engagement-dashboard
        """
        return self.call_api_get(
            "engagement-dashboard/users/new-users",
            start=start,
            end=end,
            kwargs=kwargs,
        )

    def engagement_dashboard_active_users(self, start, end, **kwargs):
        """
        Retrieve the metrics of active users in the workspace during a specific period.
        Permission required: view-engagement-dashboard
        """
        return self.call_api_get(
            "engagement-dashboard/users/active-users",
            start=start,
            end=end,
            kwargs=kwargs,
        )

    def engagement_dashboard_chat_busier_hourly(self, start, **kwargs):
        """
        Retrieve hourly data when chat is busier.
        Permission required: view-engagement-dashboard
        """
        return self.call_api_get(
            "engagement-dashboard/users/chat-busier/hourly-data",
            start=start,
            kwargs=kwargs,
        )

    def engagement_dashboard_chat_busier_weekly(self, start, **kwargs):
        """
        Retrieves weekly data when chat is busier.
        Permission required: view-engagement-dashboard
        """
        return self.call_api_get(
            "engagement-dashboard/users/chat-busier/weekly-data",
            start=start,
            kwargs=kwargs,
        )

    def engagement_dashboard_users_by_time_of_day(self, start, end, **kwargs):
        """
        Retrieve users by hours at a particular time of the day in a week.
        Permission required: view-engagement-dashboard
        """
        return self.call_api_get(
            "engagement-dashboard/users/users-by-time-of-the-day-in-a-week",
            start=start,
            end=end,
            kwargs=kwargs,
        )
