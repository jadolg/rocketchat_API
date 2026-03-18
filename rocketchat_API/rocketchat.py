# -*-coding:utf-8-*-

from rocketchat_API.APISections.assets import RocketChatAssets
from rocketchat_API.APISections.banners import RocketChatBanners
from rocketchat_API.APISections.channels import RocketChatChannels
from rocketchat_API.APISections.chat import RocketChatChat
from rocketchat_API.APISections.dm import RocketChatDM
from rocketchat_API.APISections.custom_emoji import RocketChatCustomEmoji
from rocketchat_API.APISections.groups import RocketChatGroups
from rocketchat_API.APISections.integrations import RocketChatIntegrations
from rocketchat_API.APISections.invites import RocketChatInvites
from rocketchat_API.APISections.licenses import RocketChatLicenses
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
from rocketchat_API.APISections.users_engagement import RocketChatUsersEngagement


class RocketChat(
    RocketChatAssets,
    RocketChatBanners,
    RocketChatChannels,
    RocketChatChat,
    RocketChatDM,
    RocketChatCustomEmoji,
    RocketChatGroups,
    RocketChatIntegrations,
    RocketChatInvites,
    RocketChatLicenses,
    RocketChatLivechat,
    RocketChatMiscellaneous,
    RocketChatPermissions,
    RocketChatRoles,
    RocketChatRooms,
    RocketChatSettings,
    RocketChatStatistics,
    RocketChatSubscriptions,
    RocketChatTeams,
    RocketChatUsers,
    RocketChatUsersEngagement,
):
    pass
