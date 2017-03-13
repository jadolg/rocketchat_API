from pprint import pprint

from rocketchat_API.rocketchat import RocketChat

rocket = RocketChat('mybot', 'qweqwe123!')
pprint(rocket.me().json())
# pprint(rocket.info().json())
# pprint(rocket.users_info('AFmxxCpmAj5pgSoBy').json())
# pprint(rocket.chat_post_message('GENERAL', 'hola por aqui', alias='jorge').json())
# pprint(rocket.chat_delete('GENERAL', 'KnjiERFALoE5rh4oD').json())
# pprint(rocket.chat_update('GENERAL', 'kkhiGNohm27yqJFXZ', ':D').json())
# pprint(rocket.channels_info('GENERAL').json())
# pprint(rocket.channels_history('GENERAL', count=1).json())
# pprint(rocket.channels_list().json())
# pprint(rocket.im_list().json())
# pprint(rocket.im_history(room_id='AFmxxCpmAj5pgSoByRsiuHzzh24MKTTQkw', oldest='2017-03-12T05:28:33.662Z').json())
# pprint(rocket.chat_post_message('AFmxxCpmAj5pgSoByRsiuHzzh24MKTTQkw', ';)').json())
# pprint(rocket.groups_list().json())
# pprint(rocket.groups_history('7rqeNcGj6QRbnMFfM', oldest='2017-03-12T05:48:37.530Z').json())
#
# pprint(rocket.users_list().json())
# pprint(rocket.users_get_presence('RsiuHzzh24MKTTQkw').json())
# pprint(rocket.channels_list_joined().json())
# pprint(rocket.logout().json())
