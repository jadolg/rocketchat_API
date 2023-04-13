# -*-coding:utf-8-*-

from rocketchat_API.APISections.assets import RocketChatAssets
from rocketchat_API.APISections.banners import RocketChatBanners
from rocketchat_API.APISections.channels import RocketChatChannels
from rocketchat_API.APISections.chat import RocketChatChat
from rocketchat_API.APISections.groups import RocketChatGroups
from rocketchat_API.APISections.im import RocketChatIM
from rocketchat_API.APISections.integrations import RocketChatIntegrations
from rocketchat_API.APISections.invites import RocketChatInvites
from rocketchat_API.APISections.livechat import RocketChatLivechat
from rocketchat_API.APISections.miscellaneous import RocketChatMiscellaneous
from rocketchat_API.APISections.permissions import RocketChatPermissions
from rocketchat_API.APISections.roles import RocketChatRoles
from rocketchat_API.APISections.rooms import RocketChatRooms
from rocketchat_API.APISections.settings import RocketChatSettings
from rocketchat_API.APISections.statistics import RocketChatStatistics
from rocketchat_API.APISections.subscriptions import RocketChatSubscriptions
from rocketchat_API.APISections.teams import RocketChatTeams
from rocketchat_API.APISections.users import RocketChatUsers
from rocketchat_API.APISections.video_conferences import RocketChatVideConferences


class RocketChat(
    RocketChatUsers,
    RocketChatChat,
    RocketChatChannels,
    RocketChatGroups,
    RocketChatIM,
    RocketChatIntegrations,
    RocketChatStatistics,
    RocketChatMiscellaneous,
    RocketChatSettings,
    RocketChatRooms,
    RocketChatSubscriptions,
    RocketChatAssets,
    RocketChatPermissions,
    RocketChatInvites,
    RocketChatVideConferences,
    RocketChatLivechat,
    RocketChatTeams,
    RocketChatRoles,
    RocketChatBanners,
):
    pass
