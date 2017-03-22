from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
rocket = RocketChat('akiel', 'cogitoergosum1!')
# pprint(rocket.groups_list().json())
# pprint(rocket.groups_set_read_only(room_id='BMbcw9DQNjjNhrPQY',read_only=False).json())
# pprint(rocket.groups_unarchive(room_id='BMbcw9DQNjjNhrPQY'))
# pprint(rocket.groups_set_topic(room_id='BMbcw9DQNjjNhrPQY',topic='cosas de té'))
# pprint(rocket.channels_set_type(room_id='BMbcw9DQNjjNhrPQY', a_type='p').json())

# pprint(rocket.groups_create(name='nuevo_grupo').json())
# pprint(rocket.groups_leave(room_id='YNEbvr5ToahnejTpn').json())
# pprint(rocket.groups_list().json())